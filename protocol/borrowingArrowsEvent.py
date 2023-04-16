import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("草船借箭")
async def getPlayerBorrowingArrowsEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "剩余军功": result.GetValue("borrowingarrowseventinfo.arrowsleft", 0),
            "总军功": result.GetValue("borrowingarrowseventinfo.arrowstotal", 0),
            "钥匙": result.GetValue("borrowingarrowseventinfo.stagestatus"),
            "钥匙数量": result.GetValue("borrowingarrowseventinfo.unlocknum", 0),
            "宝箱": result.GetValueList("borrowingarrowseventinfo.exchangereward"),
            "状态": result.GetValue("borrowingarrowseventinfo.currentstream", 0),
            "免费发船": result.GetValue("borrowingarrowseventinfo.boatnum", 0),
            "发船花费金币": result.GetValue("borrowingarrowseventinfo.buyboatcost", 0),
            "承重": result.GetValue("borrowingarrowseventinfo.arrowsboat", 0),
            "承重上限": result.GetValue("borrowingarrowseventinfo.boatcapacity", 0),
        }
        return info


@ProtocolMgr.Protocol("发船")
async def setSail(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        if cost > 0:
            account.logger.info("花费%d金币, 发船", cost)
        else:
            account.logger.info("免费, 发船")


@ProtocolMgr.Protocol("选择区域", ("streamId",))
async def choiceStream(account: 'Account', result: 'ServerResult', streamId):
    choice_tuple = ("下游", "中游", "上游")
    if result and result.success:
        msg = [f"选择{choice_tuple[streamId]}, 承重+{result.GetValue('borrowingarrows.arrowsstream')}"]
        if result.GetValue("borrowingarrows.borrowingresult") == 0:
            msg.append("超重")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("返航")
async def deliverArrows(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("返航")


@ProtocolMgr.Protocol("领取钥匙", ("keyId",))
async def getKey(account: 'Account', result: 'ServerResult', keyId):
    if result and result.success:
        account.logger.info("领取钥匙")


@ProtocolMgr.Protocol("开启宝箱", ("rewardType",))
async def unlockReward(account: 'Account', result: 'ServerResult', rewardType):
    reward_tuple = ("镔铁", "点卷", "宝物", "宝石")
    if result and result.success:
        account.logger.info("开启[%s]宝箱", reward_tuple[rewardType])


@ProtocolMgr.Protocol("邀功", ("rewardType",))
async def exchangeReward(account: 'Account', result: 'ServerResult', rewardType, cost=0):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("花费%s军功, 邀功, 获得%s", cost, reward_info)
