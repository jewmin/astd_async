import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("阅兵庆典")
async def getParadeEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "免费阅兵次数": result.GetValue("freetimes"),
            "免费阅兵轮数": result.GetValue("freeroundtimes"),
            "阅兵花费金币": result.GetValue("cost"),
            "购买轮数花费金币": result.GetValue("roundcost"),
            "奖励": result.GetValue("paradestate"),
        }
        return info


@ProtocolMgr.Protocol("领取阅兵奖励", ("rewardId",))
async def getParadeReward(account: 'Account', result: 'ServerResult', rewardId):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("领取阅兵奖励, 获得%s", reward_info)


@ProtocolMgr.Protocol("购买阅兵轮数")
async def addRoundTimes(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        account.logger.info("花费%d金币, 购买阅兵轮数", cost)


@ProtocolMgr.Protocol("开始阅兵")
async def paradeArmy(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        msg = f"花费{cost}金币, 开始阅兵, 获得{reward_info}"
        if "bigreward" in result.result:
            big_reward_info = RewardInfo(result.result["bigreward"]["rewardinfo"])  # noqa: F405
            msg += f" {big_reward_info}"
        account.logger.info(msg)


@ProtocolMgr.Protocol("下一位武将")
async def getNextGeneral(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("下一位武将[%s]准备阅兵", result.GetValue("generalname"))
