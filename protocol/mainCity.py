import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
import protocol.tickets as tickets
import logic.Format as Format
from model.enum.TaskType import TaskType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("主城信息", sub_module=False)
async def mainCity(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.UpdateCityInfo(result.result)


@ProtocolMgr.Protocol("升级建筑", ("player_BuildingId",))
async def upgradeLevel(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        main_city_dto: MainCityDto = kwargs["main_city_dto"]  # noqa: F405
        account.logger.info("花费%d银币, 升级建筑[%s]", main_city_dto.nextcopper, main_city_dto.buildname)


@ProtocolMgr.Protocol("领取版本更新奖励")
async def getUpdateReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.version_gift = False


@ProtocolMgr.Protocol("试试手气")
async def getPerDayReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.perdayreward = False
        gold = result.result["gold"]
        goldxs = result.result["goldxs"]
        token = result.result["token"]
        tokenxs = result.result["tokenxs"]
        account.logger.info("试试手气, 获得金币+%s(%s倍暴击), 军令+%s(%s倍暴击)", gold, goldxs, token, tokenxs)


@ProtocolMgr.Protocol("登录送礼")
async def getLoginRewardInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        if result.result["lastmonth"]["state15"] == "1":
            await getReward(account, cId=1, opt=1)
        if result.result["lastmonth"]["statefull"] == "1":
            await getReward(account, cId=1, opt=2)
        if result.result["curmonth"]["state15"] == "1":
            await getReward(account, cId=2, opt=1)
        if result.result["curmonth"]["statefull"] == "1":
            await getReward(account, cId=2, opt=2)


@ProtocolMgr.Protocol("领取登录送礼", ("cId", "opt"))
async def getReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("领取登录送礼, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("争霸风云榜")
async def getChampionInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        if result.result["canvisit"] == "1":
            await visitChampion(account)


@ProtocolMgr.Protocol("恭贺")
async def visitChampion(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("恭贺, 获得点券+%s", Format.GetShortReadable(result.result["tickets"]))


@ProtocolMgr.Protocol("将军塔")
async def getGeneralTowerInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.generaltower.HandleXml(result.result["generaltower"])
        account.logger.info("今天获得宝石+%s", Format.GetShortReadable(account.user.generaltower.gemstonenum))


@ProtocolMgr.Protocol("筑造将军塔", ("buildMode",))
async def useBuildingStone(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.generaltower.HandleXml(result.result["generaltower"])
        account.logger.info("筑造将军塔, %s", account.user.generaltower)


@ProtocolMgr.Protocol("征义兵")
async def rightArmy(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.rightcd = int(result.result.get("rightcd", 0))
        account.user.rightnum = int(result.result.get("rightnum", 0))
        forces = int(result.result.get("forces", 0))
        account.logger.info("征义兵, 获得兵力+%s, 剩余%d次征义兵", Format.GetShortReadable(forces), account.user.rightnum)


async def doDraught(account: 'Account', percent: float):
    need_forces = int(account.user.maxforce * percent)
    if account.user.forces < need_forces:
        forces = need_forces - account.user.forces
        need_copper = int(forces / 2)
        while need_copper > account.user.copper:
            await tickets.doGetTicketsReward(account, "银币", 1)

    return await draught(account, forceNum=forces)


@ProtocolMgr.Protocol("征兵", ("forceNum",))
async def draught(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("征兵, 兵力+%s", Format.GetShortReadable(kwargs["forceNum"]))


@ProtocolMgr.Protocol("征收")
async def perImpose(account: 'Account', result: 'ServerResult', kwargs: dict):
    impose_num, force_impose_cost = 0, 100
    if result.success:
        account.user.imposedto.HandleXml(result.result["imposedto"])
        impose_num = account.user.imposedto.imposenum
        force_impose_cost = account.user.imposedto.forceimposecost
        account.logger.info("今日可征收次数：%d/%d, 强征需要花费%d金币", impose_num, account.user.imposedto.imposemaxnum, force_impose_cost)
        if "larrydto" in result.result:
            effect1 = result.result["larrydto"]["effect1"]
            effect2 = result.result["larrydto"]["effect2"]
            opt = account.user.get_impose_select_le(effect1, effect2)
            await selectLE(account, opt=opt, desc=f"征收问题[({effect1}), ({effect2})]")

    return impose_num, force_impose_cost


@ProtocolMgr.Protocol("回答征收问题", ("opt",))
async def selectLE(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        le = LeDto()  # noqa: F405
        le.HandleXml(result.result["ledto"])
        account.logger.info("%s, 选择答案[%d], 获得%s", kwargs["desc"], kwargs["opt"], le)


def _impose(account: 'Account', result: 'ServerResult', desc: str):
    account.logger.info("%s, 获得银币+%s, 金币+%s", desc, Format.GetShortReadable(result.result['cooperdis']), Format.GetShortReadable(result.result["golddis"]))


@ProtocolMgr.Protocol("普通征收")
async def impose(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.add_task_finish_num(TaskType.Impose, 1)
        _impose(account, result, "征收")


@ProtocolMgr.Protocol("强制征收")
async def forceImpose(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.add_task_finish_num(TaskType.ForceImpose, 1)
        _impose(account, result, "强征")


@ProtocolMgr.Protocol("重置武将兵力", ("generalId", "forceNum"))
async def resetSoldier(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("把武将[%s]的兵力设置为%d", kwargs["generalName"], kwargs["forceNum"])
