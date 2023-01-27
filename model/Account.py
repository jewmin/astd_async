import asyncio
import logic.Format as Format
import engine.LogManager as LogManager
from manager.TimeMgr import TimeMgr
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

    async def Login(self) -> None:
        import manager.LoginMgr as LoginMgr
        cookies = {}
        login_result = await LoginMgr.Login(self, cookies)
        if login_result is None:
            self.logger.info("登录失败，请重试")
            self.Relogin(30)
        elif login_result.status == LoginStatus.Success:
            self.InitGame(login_result)
        else:
            self.logger.info(login_result)
            self.Relogin(30)

    def Relogin(self, wait_seconds: int):
        if wait_seconds:
            self.logger.info("将在%s后开始重新登录", Format.GetSecondString(wait_seconds))
            asyncio.get_event_loop().call_later(wait_seconds, lambda: asyncio.get_event_loop().create_task(self.Login()))
        else:
            asyncio.get_event_loop().create_task(self.Login())

    def InitGame(self, login_result: LoginResult) -> None:
        self.status = AccountStatus.NotStart
        self.game_url = login_result.game_url
        self.session_id = login_result.session_id
        self.cookies = login_result.cookies
        asyncio.get_event_loop().create_task(self.InitSession())

    async def InitSession(self) -> None:
        import protocol.server as server
        self.user = User()
        self.time_mgr = TimeMgr()
        await server.getServerTime(self)
        if await server.getPlayerInfoByUserId(self):
            self.InitCompleted()
        #     self.build_services()
        #     self.build_activity()
        #     self.m_objTaskMgr.set_variables(self.m_objServiceFactory, self.m_objProtocolMgr, self.m_objUser, self)
        #     self.m_objTaskMgr.init()
        #     self.init_completed()

    def InitCompleted(self) -> None:
        self.running = True
