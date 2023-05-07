import manager.ProtocolMgr as ProtocolMgr
from logic.Format import GetShortReadable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("征收活动")
async def getEventGiftInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        for idx, reward in enumerate(result.GetValue("rewardnum")):
            if reward == 1:
                await receiveEventReward(account, id=idx)


@ProtocolMgr.Protocol("领取礼包", ("id",))
async def receiveEventReward(account: 'Account', result: 'ServerResult', id):
    if result and result.success:
        ticket = result.GetValue("message")
        account.logger.info("领取礼包, 获得点券+%s", GetShortReadable(ticket))
