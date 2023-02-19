import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("战兽圣殿")
async def getInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "购买1次": result.GetValue("warbeasttemple.buyonecost", 999),
            "购买10次": result.GetValue("warbeasttemple.buytencost", 999),
        }
        return dict_info


@ProtocolMgr.Protocol("购买", ("type",))
async def buy(account: 'Account', result: 'ServerResult', type, cost):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        if cost > 0:
            account.logger.info("花费%s金币购买, 获得%s", cost, reward_info)
        else:
            account.logger.info("免费购买, 获得%s", reward_info)
