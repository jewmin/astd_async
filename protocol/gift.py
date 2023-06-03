import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
from logic.Format import GetShortReadable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("征收活动")
async def getEventGiftInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        rewardnum = result.GetValue("rewardnum")
        if rewardnum:
            for idx, reward in enumerate(rewardnum):
                if reward == 1:
                    await receiveEventReward(account, id=idx)


@ProtocolMgr.Protocol("领取礼包", ("id",))
async def receiveEventReward(account: 'Account', result: 'ServerResult', id):
    if result.success:
        ticket = result.GetValue("message")
        account.logger.info("领取礼包, 获得点券+%s", GetShortReadable(ticket))


@ProtocolMgr.Protocol("军资回馈")
async def getRepayEventGiftInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "奖励": result.GetValueList("reward"),
            "领取状态": result.GetValueList("rewardnum"),
        }
        return info


@ProtocolMgr.Protocol("领取礼包")
async def receiveRepayEventReward(account: 'Account', result: 'ServerResult', id):
    if result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = 1
        reward.num = result.GetValue("message")
        reward.itemname = "宝石"
        reward_info.reward.append(reward)
        account.logger.info("军资回馈, 领取礼包, 获得%s", reward_info)
