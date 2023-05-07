import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("宝石倾销")
async def getDetail(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "锦囊": result.GetValue("totalbags"),
            "商品": result.GetValueList("goodlist.good")[0],
        }
        return info


@ProtocolMgr.Protocol("购买", ("id",))
async def buy(account: 'Account', result: 'ServerResult', id, good):
    if result and result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = good["baoshilevel"]
        reward.itemname = "宝石"
        reward.num = 1
        reward_info.reward.append(reward)
        account.logger.info("花费%d点券, 获得锦囊+%d, %s", good["cost"], good["extrabags"], reward_info)


@ProtocolMgr.Protocol("开启锦囊", ("num",))
async def openBags(account: 'Account', result: 'ServerResult', num):
    if result and result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = 1
        reward.itemname = "宝石"
        reward.num = 0
        for baoshi in result.GetValueList("baoshi"):
            reward.num += baoshi["num"]
        reward_info.reward.append(reward)
        account.logger.info("打开%d个锦囊, 获得%s", num, reward_info)
