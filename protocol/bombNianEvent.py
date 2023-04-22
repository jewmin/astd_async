import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("抓年兽")
async def getBombNianInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "领奖状态": result.GetValue("canget"),
        }
        if info["领奖状态"] == 1:
            info["奖励"] = result.GetValueList("reward")
        else:
            info["年兽血量"] = result.GetValue("playerbombnianeventinfo.nianhp")
            info["年兽最大血量"] = result.GetValue("playerbombnianeventinfo.nianmaxhp")
            info["鞭炮"] = [{
                "类型": 1,
                "免费次数": result.GetValue("playerbombnianeventinfo.firecrackersnum"),
                "花费金币": result.GetValue("cost.firecrackerscost"),
            }, {
                "类型": 2,
                "免费次数": result.GetValue("playerbombnianeventinfo.stringfirecrackersnum"),
                "花费金币": result.GetValue("cost.stringfirecrackerscost"),
            }, {
                "类型": 3,
                "免费次数": result.GetValue("playerbombnianeventinfo.springthundernum"),
                "花费金币": result.GetValue("cost.springthundercost"),
            }]
        if "playerrank" in result.result:
            info["排名奖励状态"] = result.GetValue("getrankreward")
        return info


@ProtocolMgr.Protocol("捡起奖励", ("giftId",))
async def openGift(account: 'Account', result: 'ServerResult', giftId):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("捡起奖励, 获得%s", reward_info)


@ProtocolMgr.Protocol("放鞭炮", ("bombType",))
async def bombNian(account: 'Account', result: 'ServerResult', bombType, cost=0):
    if result and result.success:
        reward_info = RewardInfo(result.result["bombnianreward"]["rewardinfo"])  # noqa: F405
        account.logger.info("花费%d金币, 放鞭炮, 获得%s", cost, reward_info)


@ProtocolMgr.Protocol("捕抓年兽")
async def huntNian(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        if result.GetValue("huntstate", 0) == 1:
            reward_info = RewardInfo(result.result["huntnianreward"]["rewardinfo"])  # noqa: F405
            account.logger.info("捕抓年兽成功, 获得%s", reward_info)
        else:
            account.logger.info("捕抓年兽失败")


@ProtocolMgr.Protocol("领取排名奖励")
async def getRankReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        reward_info = RewardInfo(result.result["rankreward"]["rewardinfo"])  # noqa: F405
        account.logger.info("领取年兽排名奖励, 获得%s", reward_info)
