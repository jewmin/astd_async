from functools import wraps
import manager.TransferMgr as TransferMgr
from model.Account import Account
from model.ServerResult import ServerResult
from model.enum.AccountStatus import AccountStatus

GET  = 1
POST = 2


def Protocol(method: int, desc: str):
    assert method in (GET, POST), "请求类型必须是GET或POST"

    def request(func):

        @wraps(func)
        async def call(account: Account, *args, **kwargs):
            module = func.__module__.replace("protocol.", "")
            real_url = f"{account.game_url}root/{module}!{func.__name__}.action?{account.time_mgr.GetTimestamp()}"

            if method == GET:
                server_result = await _GetXml(real_url, desc, account.cookies)
                _HandleResult(account, server_result, desc)
            else:
                server_result = await _PostXml(real_url, kwargs, desc, account.cookies)
                _HandleResult(account, server_result, desc, kwargs)

            return await func(account, server_result)

        return call

    return request


async def _GetXml(url: str, desc: str, cookies: dict) -> ServerResult:
    return ServerResult(url, await TransferMgr.Get(url, cookies))


async def _PostXml(url: str, data: dict, desc: str, cookies: dict) -> ServerResult:
    return ServerResult(url, await TransferMgr.Post(url, data, cookies))


def _HandleResult(account: Account, server_result: ServerResult, desc: str, data: dict = None):
    log_dict = {}
    if data is None:
        log_dict["type"] = "GET"
    else:
        log_dict["type"] = "POST"
        log_dict["data"] = data
    log_dict["desc"] = desc
    log_dict["url"] = server_result.GetUrl()
    log_dict["result"] = server_result.GetDebugInfo()
    account.logger.debug(log_dict)

    if not server_result.IsHttpSucceed():
        return

    if server_result.success:
        if "playerupdateinfo" in server_result.result:
            account.user.UpdatePlayerInfo(server_result.result["playerupdateinfo"])
        if "playerbattleinfo" in server_result.result:
            account.user.UpdatePlayerBattleInfo(server_result.result["playerbattleinfo"])

    elif "验证码" in server_result.error:
        account.running = False
        account.status = AccountStatus.StoppedGameVerify
        account.Relogin(1800)
        raise RuntimeError("需要验证码")

    elif "连接已超时" in server_result.error or "用户已在别处登陆" in server_result.error:
        account.running = False
        account.Relogin(1800)
        raise RuntimeError("需要重新登录")

    else:
        raise RuntimeError(server_result.error)
