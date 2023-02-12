import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("礼包", ("type",))
async def getNewGiftList(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        if "weekendgift" in result.result:
            gift = result.result["weekendgift"]
            await getNewGiftReward(account, giftId=gift["id"])
        if "gift" in result.result:
            gift = result.result["gift"]
            if not isinstance(gift, list):
                gift = [gift]
            for g in gift:
                if g["intime"] == "1" and g["statuts"] == "0":
                    await getNewGiftReward(account, giftId=g["id"])


async def doGetNewGiftList(account: 'Account'):
    await getNewGiftList(account, type=0)
    await getNewGiftList(account, type=1)


@ProtocolMgr.Protocol("领取礼包", ("giftId",))
async def getNewGiftReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        content = result.result.get("content", "无效奖励")
        account.logger.info("领取礼包, 获得%s", content)
