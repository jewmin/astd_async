import asyncio
import engine.LogManager as LogManager
import logic.Format as Format
from manager.TimeMgr import TimeMgr
from manager.TaskMgr import TaskMgr
import manager.LoginMgr as LoginMgr
import protocol.server as server
import task
from model.User import User
from model.LoginResult import LoginResult
from model.enum.ServerType import ServerType
from model.enum.LoginStatus import LoginStatus
from model.enum.AccountStatus import AccountStatus


class Account:
    """账号信息"""
    def __init__(self, server_type: ServerType, server_id: int, username: str, password: str, rolename: str):
        self.logger = LogManager.CommonLoggerAdapter(LogManager.GetLogger(self.__class__.__name__), {"username": username, "rolename": rolename}, "[username: %(username)s, rolename: %(rolename)s]")
        self.server_type = server_type
        self.server_id = server_id
        self.username = username
        self.password = password
        self.rolename = rolename
        self.status: AccountStatus = None
        self.game_url: str = None
        self.session_id: str = None
        self.cookies: dict = None
        self.running = False
        self.user: User = None
        self.time_mgr: TimeMgr = None
        self.task_mgr: TaskMgr = None

    async def Login(self) -> None:
        cookies = {}
        login_result = await LoginMgr.Login(self, cookies)
        if login_result is None:
            self.logger.info("登录失败，请重试")
            self.Relogin(30)
        elif login_result.status == LoginStatus.Success:
            await self.InitGame(login_result)
        else:
            self.logger.info(login_result)
            self.Relogin(30)

    def Relogin(self, wait_seconds: int):
        if wait_seconds:
            self.logger.info("将在%s后开始重新登录", Format.GetSecondString(wait_seconds))
            asyncio.get_event_loop().call_later(wait_seconds, lambda: asyncio.get_event_loop().create_task(self.Login()))
        else:
            asyncio.get_event_loop().create_task(self.Login())

    async def InitGame(self, login_result: LoginResult) -> None:
        self.status = AccountStatus.NotStart
        self.game_url = login_result.game_url
        self.session_id = login_result.session_id
        self.cookies = login_result.cookies
        await self.InitSession()

    async def InitSession(self) -> None:
        self.user = User()
        self.time_mgr = TimeMgr()
        self.task_mgr = TaskMgr()
        await server.getServerTime(self)
        if await server.getPlayerInfoByUserId(self):
            await self.AddTasks()
            self.InitCompleted()

    def InitCompleted(self) -> None:
        self.running = True
        self.task_mgr.RunAllTasks()

    async def AddTasks(self) -> None:
        for task_class in task.__all__:
            self.task_mgr.AddTask(task_class(self))
        for t in self.task_mgr.tasks.values():
            await t.Init()
