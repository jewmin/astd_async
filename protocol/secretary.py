import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("秘书", sub_module=False)
async def secretary(account: 'Account', result: 'ServerResult'):
    if result.success:
        max_token_num = int(result.result.get("maxtokennum", 0))
        token_num = int(result.result.get("tokennum", 0))
        cd = int(result.result.get("cd", 0))
        if max_token_num - token_num > 0 and cd == 0:
            await applyToken(account)


@ProtocolMgr.Protocol("领取每日军令")
async def applyToken(account: 'Account', result: 'ServerResult'):
    if result.success:
        max_token_num = int(result.result.get("maxtokennum", 0))
        token_num = int(result.result.get("tokennum", 0))
        cd = int(result.result.get("cd", 0))
        account.logger.info("领取每日军令, 还有%d个, 领取CD: %s", max_token_num - token_num, account.time_mgr.GetDatetimeString(cd))
