import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("新春拜年")
async def getMemoryEventInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "拜年免费次数": result.GetValue("freetimes", 0),
            "拜年花费金币": result.GetValue("wishcost", 100),
            "红包": result.GetValueList("hongbao"),
            "回忆图": result.GetValueList("picreward"),
            "点亮武将": result.GetValue("general"),
        }
        return info


@ProtocolMgr.Protocol("拜年")
async def newYearVisit(account: 'Account', result: 'ServerResult', gold=0):
    if result.success:
        name = result.GetValue("name")
        light = result.GetValue("light", 0)
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        msg = []
        if gold > 0:
            msg.append(f"花费{gold}金币")
        else:
            msg.append("免费")
        msg.append("新春拜年")
        msg.append(f"和武将[{name}]拜年")
        if light:
            msg.append("点亮武将")
        msg.append(f"获得{reward_info}")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("回忆图", ("rewardId",))
async def openPicReward(account: 'Account', result: 'ServerResult', rewardId):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("新春拜年, 领取回忆图奖励, 获得%s", reward_info)


@ProtocolMgr.Protocol("红包", ("type",))
async def openHongbao(account: 'Account', result: 'ServerResult', type, gold=0):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        msg = []
        if gold > 0:
            msg.append(f"花费{gold}金币")
        else:
            msg.append("免费")
        msg.extend(["新春拜年", "领取红包", f"获得{reward_info}"])
        account.logger.info(", ".join(msg))
