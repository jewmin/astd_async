import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
import logic.Format as Format

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("升官", sub_module=False)
async def officer(account: 'Account', result: 'ServerResult'):
    if result.success:
        if result.result["savesalary_cd"] == "0":
            await saveSalary(account)


@ProtocolMgr.Protocol("领取俸禄")
async def saveSalary(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取俸禄, 获得银币+%s, %s %s", Format.GetShortReadable(result.result["gain"]), result.result["troop"], RewardInfo(result.result["rewardinfo"]))  # noqa: F405
