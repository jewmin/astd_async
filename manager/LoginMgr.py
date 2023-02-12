from login.LoginBase import LoginBase
from login.YaoWanLogin import YaoWanLogin
from model.enum.ServerType import ServerType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account


def GetLoginImpl(server_type: ServerType) -> LoginBase:
    if server_type == ServerType.YaoWan:
        return YaoWanLogin()
    raise NotImplementedError(f"未知服务器类型{server_type}")


async def Login(account: 'Account', cookies: dict):
    partner = GetLoginImpl(account.server_type)
    partner.SetAccount(account)
    try:
        return await partner.Login(cookies)
    except Exception:
        account.logger.LogLastExcept()
        return None
