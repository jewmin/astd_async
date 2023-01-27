import manager.ProtocolMgr as ProtocolMgr
from model.Account import Account
from model.ServerResult import ServerResult


@ProtocolMgr.Protocol(ProtocolMgr.GET, "领取版本更新奖励")
async def getUpdateReward(account: Account, result: ServerResult):
    if result.success:
        account.user.version_gift = False
