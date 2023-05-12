import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("攻坚战")
async def getNationTaskNewInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "状态": result.GetValue("status"),
            "集结城池": result.GetValue("masscity", ""),
        }
        return dict_info


@ProtocolMgr.Protocol("领取攻坚战奖励")
async def getNationTaskNewReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取攻坚战奖励, 国家宝箱+%d", result.GetValue("box", 0))
