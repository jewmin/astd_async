import re
import manager.TransferMgr as TransferMgr
from login.LoginBase import LoginBase
from model.LoginResult import LoginResult
from model.enum.LoginStatus import LoginStatus

YaoWanUrl = {
    218: "要玩218区",
    219: "要玩219区",
    272: "傲视争霸区",
    470: "CJ专属服",
    500: "虎贲营",
    1000: "龍",
}


class YaoWanLogin(LoginBase):
    """要玩登录"""
    def __init__(self):
        super().__init__()

    async def Login(self, cookies: dict) -> LoginResult:
        self.LoggingIn()
        login_result = LoginResult()
        url = "http://www.yaowan.com/?m=user&action=loginform&subdomain=as"
        data = {"username": self.account.username, "password": self.account.password}
        resp = await TransferMgr.PostPure(url, data, cookies)
        if resp is None:
            login_result.status = LoginStatus.FailInLogin
            return login_result

        content = await resp.text()
        if content.startswith("<script>"):
            login_result.status = LoginStatus.FailInLogin
            return login_result

        self.FindingServerUrl()
        server_url = await self.GetServerUrl(cookies)
        if not server_url:
            login_result.status = LoginStatus.FailInFindingGameUrl
            return login_result

        await self.ProcessRedirect(server_url, login_result, cookies)
        return login_result

    async def GetServerUrl(self, cookies: dict) -> str:
        url = "http://as.yaowan.com/as_server_list.html"
        filename = "yao_wan_as_server_list.html"
        content = self.GetCacheFile(filename)
        if not content:
            return await self.GetAndSaveUrl(url, cookies, filename)

        game_url = self.FindServerUrlFromString(content)
        if not game_url:
            return await self.GetAndSaveUrl(url, cookies, filename)

        return game_url

    async def GetAndSaveUrl(self, url: str, cookies: dict, filename: str) -> str:
        resp = await TransferMgr.GetPure(url, cookies)
        if resp is None:
            return

        content = await resp.text()
        game_url = self.FindServerUrlFromString(content)
        if not game_url:
            return

        self.SaveCacheFile(filename, content)
        return game_url

    def FindServerUrlFromString(self, content: str) -> str:
        name = YaoWanUrl.get(self.account.server_id, f"双线{self.account.server_id}区")
        compiler = re.compile(f"<a.*href=\"(.*?)\".*>({name}.*)</a>")
        search = re.search(compiler, content)
        if search is None:
            return

        match = search.groups()
        if match is None or len(match) < 2:
            return

        return match[0]
