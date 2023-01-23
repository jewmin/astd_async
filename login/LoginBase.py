import os
from urllib.parse import urlparse
from aiohttp import ClientResponse
import engine.LogManager as LogManager
import manager.TransferMgr as TransferMgr
from model.Account import Account
from model.LoginResult import LoginResult
from model.enum.LoginStatus import LoginStatus


def MakeSureValidUrl(base_url: str, now_url: str) -> str:
    if now_url.startswith("http://") or now_url.startswith("https://"):
        return now_url

    result = urlparse(base_url)
    scheme = result.scheme
    netloc = result.netloc
    path = result.path
    if (index := path.rfind("/")) >= 0:
        path = path[:index]

    if now_url.startswith("./"):
        now_url = now_url[1:]

    elif now_url.startswith("../"):
        now_url = now_url[2:]
        if (index := path.rfind("/")) >= 0:
            path = path[:index]

    elif now_url.startswith("/"):
        path = ""

    else:
        now_url = f"/{now_url}"

    return f"{scheme}://{netloc}{path}{now_url}"


class LoginBase:
    """登录基类"""
    def __init__(self):
        self.logger = LogManager.GetLogger(self.__class__.__name__)
        self.account: Account = None

    def SetAccount(self, account: Account) -> None:
        self.logger = LogManager.CommonLoggerAdapter(self.logger, {"username": account.username, "rolename": account.rolename}, "[username: %(username)s, rolename: %(rolename)s]")
        self.account = account

    def SaveCacheFile(self, filename: str, content: str) -> None:
        folder = "./bin/cache"
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(f"{folder}/{filename}", "w", encoding="utf-8") as fs:
            fs.write(content)

    def GetCacheFile(self, filename: str) -> str:
        folder = "./bin/cache"
        if not os.path.exists(folder):
            os.mkdir(folder)
        filepath = f"{folder}/{filename}"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as fs:
                return fs.read()

    async def Login(self, cookies: dict) -> LoginResult:
        raise NotImplementedError("必须实现此函数")

    async def ProcessRedirect(self, redirect_url: str, login_result: LoginResult, cookies: dict) -> None:
        self.GoingToGameUrl()
        resp = await TransferMgr.GetPure(redirect_url, cookies)
        if resp is None:
            login_result.status = LoginStatus.FailInGoToGameUrl
            return

        location = resp.headers.get("location")
        if location is None:
            login_result.status = LoginStatus.FailInGetSession
            self.logger.error(await resp.text())
            return

        location = MakeSureValidUrl(redirect_url, location)
        if "start.action" not in location:
            await self.ProcessRedirect(location, login_result, cookies)
        else:
            await self.ProcessStartGame(location, login_result, cookies)

    async def ProcessStartGame(self, start_url: str, login_result: LoginResult, cookies: dict) -> None:
        self.GettingSession()
        resp = await TransferMgr.GetPure(start_url, cookies)
        self.HandleStartGame(resp, login_result, cookies)

    def HandleStartGame(self, resp: ClientResponse, login_result: LoginResult, cookies: dict):
        if resp is None:
            login_result.status = LoginStatus.FailInGetSession
            return

        login_result.game_url = resp.headers["location"]
        login_result.session_id = resp.cookies["JSESSIONID"]
        login_result.cookies = cookies
        if not login_result.session_id:
            login_result.status = LoginStatus.FailInGetSession
            return

        login_result.status = LoginStatus.Success
        self.Succeed()

    def LoggingIn(self):
        self.logger.info("正在登录...")

    def FindingServerUrl(self):
        self.logger.info("正在获取所在区的地址...")

    def GoingToGameUrl(self):
        self.logger.info("正在跳转到所在区地址...")

    def GettingSession(self):
        self.logger.info("正在获取会话...")

    def Succeed(self):
        self.logger.info("登录完成~~")
