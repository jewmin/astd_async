import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
from model.enum.TaskType import TaskType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("御用精纺厂")
async def royaltyWeaveInfo2(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "行动力状态": result.GetValue("activestatus"),
            "消耗行动力": result.GetValue("needactive"),
            "剩余高效次数": result.GetValue("remainhigh"),
            "高效次数": result.GetValue("high"),
            "剩余极限次数": result.GetValue("remainlimit"),
            "极限次数": result.GetValue("limit"),
            "布匹": result.GetValue("weavenum"),
            "布匹上限": result.GetValue("maxnum"),
            "换购消耗布匹": result.GetValue("needweavenum"),
            "商人": result.GetValue("tradername"),
            "刷新商人费用": result.GetValue("cost"),
            "换购商品": RewardInfo(result.result["rewardinfo"]),  # noqa: F405
        }
        account.logger.info(
            "布匹(%d/%d)，商人(%s, 可换购%s), 可纺织次数(%d/%d)",
            dict_info["布匹"], dict_info["布匹上限"], dict_info["商人"], dict_info["换购商品"],
            dict_info["剩余极限次数"], dict_info["极限次数"])
        return dict_info


@ProtocolMgr.Protocol("一键纺织", ("times",))
async def royaltyWeave2(account: 'Account', result: 'ServerResult', times, active):
    if result and result.success:
        account.user.add_task_finish_num(TaskType.Weave, times)
        msg = f"花费{active}行动力一键纺织"
        once_num = result.GetValue("oncenum")
        bu_pi = result.GetValueList("bupi")
        for v in bu_pi:
            msg += f", 布匹+{v['modulus'] * once_num}"
        account.logger.info(msg)


@ProtocolMgr.Protocol("换购")
async def convertRoyaltyWeaveNew2(account: 'Account', result: 'ServerResult', need_weave_num):
    if result and result.success:
        account.logger.info("花费%d布匹换购, 获得%s", need_weave_num, RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("刷新换购商人")
async def refreshRoyaltyWeaveNew(account: 'Account', result: 'ServerResult', cost):
    if result and result.success:
        account.logger.info("花费%d金币刷新换购商人, 商人(%s, 可换购%s)", cost, result.result["tradername"], RewardInfo(result.result["rewardinfo"]))  # noqa: F405
