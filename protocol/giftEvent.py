import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult



@ProtocolMgr.Protocol("充值赠礼")
async def getGoldBoxEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "宝箱": result.GetValue("boxnum"),
            "在线奖励": result.GetValue("onlinereward", 0),
        }
        return info


@ProtocolMgr.Protocol("领取在线奖励")
async def recvOnlineReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("领取在线奖励, 获得宝箱+%d", result.GetValue("rewardbox"))


@ProtocolMgr.Protocol("开启充值赠礼宝箱")
async def openGoldBoxEvent(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        if "baoshi" in result.GetValue("reward"):
            account.logger.info("开启充值赠礼宝箱, 获得宝石+%d", result.GetValue("reward.baoshi"))
        elif "gold" in result.GetValue("reward"):
            account.logger.info("开启充值赠礼宝箱, 获得金币+%d", result.GetValue("reward.gold"))
        elif "ticket" in result.GetValue("reward"):
            account.logger.info("开启充值赠礼宝箱, 获得点券+%d", result.GetValue("reward.ticket"))
        else:
            account.logger.info("开启充值赠礼宝箱, 获得%s", result.result)

        if "biginfo" in result.result:
            account.logger.info("开启充值赠礼宝箱, 获得大将令[%s]+%d", result.GetValue("biginfo.name"), result.GetValue("biginfo.addnum"))
