import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("武斗庆典")
async def getKfwdEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "奖励": result.GetValue("rewardgold", 0),
        }
        return info


@ProtocolMgr.Protocol("武斗庆典奖励")
async def getKfwdReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("领取武斗庆典奖励, 获得宝箱+%d", result.GetValue("tickets"))
