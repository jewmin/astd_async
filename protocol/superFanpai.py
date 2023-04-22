import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("超级翻牌")
async def getSuperFanpaiInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "购买次数花费金币": result.GetValue("superfanpaiinfo.buyone"),
            "卡牌全开花费金币": result.GetValue("superfanpaiinfo.buyall"),
            "翻牌次数": result.GetValue("superfanpaiinfo.freetimes"),
            "翻牌": result.GetValue("superfanpaiinfo.isfanpai", 0) == 1,
            "卡牌": result.GetValueList("superfanpaiinfo.card"),
        }
        for idx, card in enumerate(info["卡牌"], 1):
            card["id"] = idx
        return info


@ProtocolMgr.Protocol("翻牌", ("cardId",))
async def fanOne(account: 'Account', result: 'ServerResult', cardId):
    if result and result.success:
        reward_info = RewardInfo()  # noqa: F405
        for card in result.GetValueList("card"):
            if card["ischoose"] == 1:
                reward = Reward()  # noqa: F405
                reward.type = 5
                reward.lv = card["gemlevel"]
                reward.num = card["gemnumber"]
                reward_info.reward.append(reward)
                break
        account.logger.info("翻牌, 获得%s", reward_info)


@ProtocolMgr.Protocol("购买次数")
async def buyTimes(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        account.logger.info("花费%d金币, 购买次数", cost)


@ProtocolMgr.Protocol("卡牌全开")
async def getAll(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = 18
        reward.num = 3
        reward_info.reward.append(reward)
        account.logger.info("花费%d金币, 卡牌全开, 获得%s", cost, reward_info)


@ProtocolMgr.Protocol("洗牌")
async def xiPai(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("洗牌")
