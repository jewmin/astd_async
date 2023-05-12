import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("中秋月饼")
async def getInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "吃货状态": result.GetValueList("eatstate"),
            "吃蛋黄月饼花费金币": result.GetValue("cost1"),
            "吃豆沙月饼花费金币": result.GetValue("cost2"),
        }
        return info


@ProtocolMgr.Protocol("吃月饼", ("type",))
async def eatMooncake(account: 'Account', result: 'ServerResult', type, cost=0):
    cake_name = ("", "蛋黄", "豆沙")
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("花费%d金币, 吃%s月饼, 获得%s", cost, cake_name[type], reward_info)


@ProtocolMgr.Protocol("领取月饼奖励", ("rewardId",))
async def getProgressReward(account: 'Account', result: 'ServerResult', rewardId):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("领取月饼奖励, 获得%s", reward_info)
