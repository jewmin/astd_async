import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
import logic.Format as Format
from model.enum.TaskType import TaskType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("高级炼制工坊")
async def getRefineBintieFactory(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "行动力状态": result.GetValue("status"),
            "消耗银币": result.GetValue("coppercost"),
            "消耗行动力": result.GetValue("needactive"),
            "剩余高效次数": result.GetValue("remainhigh"),
            "剩余极限次数": result.GetValue("remainlimit"),
            "极限次数": result.GetValue("limit"),
        }
        account.logger.info("可炼制次数(%d/%d)", dict_info["剩余极限次数"], dict_info["极限次数"])
        return dict_info


@ProtocolMgr.Protocol("炼制", ("mode",))
async def doRefineBintieFactory(account: 'Account', result: 'ServerResult', mode, copper, active):
    if result and result.success:
        account.user.add_task_finish_num(TaskType.RefineBintie, 1)
        account.logger.info("消耗%s银币, %d行动力炼制, 获得%s", Format.GetShortReadable(copper), active, RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("精炼工房")
async def getRefineInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "行动力状态": result.GetValue("status"),
            "消耗银币": result.GetValue("copper"),
            "消耗行动力": result.GetValue("needactive"),
            "剩余高效次数": result.GetValue("remainhigh"),
            "剩余极限次数": result.GetValue("remainlimit"),
            "极限次数": result.GetValue("limit"),
            "消耗余料": result.GetValue("onceplus"),
            "当前余料": result.GetValue("refinenum"),
            "余料上限": result.GetValue("maxrefinenum"),
            "升级单个工人消耗金币": result.GetValue("percost"),
            "工人们": result.GetValue("refiner"),
            "可精炼工人": False,
        }
        for v in result.GetValueList("refinergroup"):
            if v["time"] == 0:
                dict_info["可精炼工人"] = True
                break
        account.logger.info("余料库存(%d/%d)，可精炼次数(%d/%d)", dict_info["当前余料"], dict_info["余料上限"], dict_info["剩余极限次数"], dict_info["极限次数"])
        return dict_info


@ProtocolMgr.Protocol("精炼")
async def refine(account: 'Account', result: 'ServerResult', copper, active):
    if result and result.success:
        account.user.add_task_finish_num(TaskType.Refine, 1)
        msg = f"消耗{copper}银币、{active}行动力精炼"
        if "eventintro" in result.result:
            msg += f", 触发精炼事件<{result.result['eventintro']}>"
        bao_ji = result.GetValue("baoji")
        if bao_ji > 0:
            msg += f", {bao_ji}倍暴击"
        msg += f", 获得玉石+{result.result['bowlder']}"
        if "baoshi" in result.result:
            msg += f", 宝石+{result.result['baoshi']}"
        account.logger.info(msg)


@ProtocolMgr.Protocol("升级精炼工人", ("refinerOrder",))
async def refreshOneRefiner(account: 'Account', result: 'ServerResult', refinerOrder, refiner, cost):
    if result and result.success:
        account.logger.info("花费%d金币升级精炼工人[%s(%s)]", cost, refiner["name"], refiner["color"])
