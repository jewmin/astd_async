from functools import wraps
import manager.TransferMgr as TransferMgr
from model.ServerResult import ServerResult
from model.enum.AccountStatus import AccountStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account

# GET  = 1
# POST = 2


class ProtocolError(RuntimeError):
    pass


class ReloginError(RuntimeError):
    pass


def Protocol(desc: str, params: tuple = (), sub_module: bool = True):
    # assert method in (GET, POST), "请求类型必须是GET或POST"

    def request(func):

        @wraps(func)
        async def call(account: 'Account', *args, **kwargs):
            data = {}
            for param in params:
                assert param in kwargs, f"POST请求需要参数[{param}]"
                data[param] = kwargs[param]

            module = func.__module__.replace("protocol.", "")
            if sub_module:
                module += f"!{func.__name__}"
            real_url = f"{account.game_url}root/{module}.action?{account.time_mgr.GetTimestamp()}"

            retries = 3
            if data:
                while True:
                    try:
                        server_result = await _PostXml(real_url, module, data, desc, account.cookies)
                        _HandleResult(account, server_result, desc, data)
                    except ProtocolError:
                        retries -= 1
                        if retries <= 0:
                            raise
                    else:
                        break
            else:
                while True:
                    try:
                        server_result = await _GetXml(real_url, module, desc, account.cookies)
                        _HandleResult(account, server_result, desc)
                    except ProtocolError:
                        retries -= 1
                        if retries <= 0:
                            raise
                    else:
                        break

            return await func(account, server_result, **kwargs)

        return call

    return request


async def _GetXml(url: str, action: str, desc: str, cookies: dict) -> 'ServerResult':
    return ServerResult(url, action, await TransferMgr.Get(url, cookies))


async def _PostXml(url: str, action: str, data: dict, desc: str, cookies: dict) -> 'ServerResult':
    return ServerResult(url, action, await TransferMgr.Post(url, data, cookies))


def _HandleResult(account: 'Account', server_result: 'ServerResult', desc: str, data: dict = None):
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
        raise ProtocolError(server_result.GetHttpErrorInfo())

    if server_result.success:
        if "playerupdateinfo" in server_result.result:
            account.user.UpdatePlayerInfo(server_result.result["playerupdateinfo"])
        if "playerbattleinfo" in server_result.result:
            account.user.UpdatePlayerBattleInfo(server_result.result["playerbattleinfo"])

    elif "验证码" in server_result.error:
        account.status = AccountStatus.StoppedGameVerify
        raise ReloginError("需要验证码")

    elif "连接已超时" in server_result.error or "用户已在别处登陆" in server_result.error:
        raise ReloginError("需要重新登录")

    else:
        # raise ProtocolError(f"{server_result.GetUrl()} - {desc}: {server_result.error}")
        account.logger.error("%s - %s - %s: %s", server_result.GetAction(), data, desc, server_result.error)
