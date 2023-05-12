import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("培养")
async def getRefreshGeneralInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "免费白金洗次数": result.GetValue("freebaijintime"),
            "免费至尊洗次数": result.GetValue("freezizuntime"),
            "武将": result.GetValueList("general"),
        }
        return dict_info


@ProtocolMgr.Protocol("培养详情", ("generalId",))
async def getRefreshGeneralDetailInfo(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        dict_info = {
            "武将等级": result.GetValue("generaldto.generallevel"),
            "原始属性": result.GetValue("general.originalattr"),
        }
        if "newattr" in result.result["general"]:
            dict_info["新属性"] = result.GetValue("general.newattr")
        return dict_info


@ProtocolMgr.Protocol("属性确定", ("generalId", "choose"))
async def refreshGeneralConfirm(account: 'Account', result: 'ServerResult', generalId, choose):
    if result.success:
        account.logger.info(result.result["message"])


@ProtocolMgr.Protocol("洗属性", ("generalId", "refreshModel"))
async def refreshGeneral(account: 'Account', result: 'ServerResult', generalId, refreshModel):
    if result.success:
        dict_info = {
            "新属性": {
                "plusforces": result.GetValue("general.plusforces"),
                "plusintelligence": result.GetValue("general.plusintelligence"),
                "plusleader": result.GetValue("general.plusleader"),
            }
        }
        return dict_info


@ProtocolMgr.Protocol("觉醒详情", ("generalId",))
async def getAwakenGeneralInfo(account: 'Account', result: 'ServerResult', generalId):
    if result.success:
        dict_info = {
            "免费觉醒酒": result.GetValue("generalawakeinfo.freeliquornum"),
            "需要觉醒酒": result.GetValue("generalawakeinfo.needliquornum"),
            "拥有觉醒酒": result.GetValue("generalawakeinfo.liquornum"),
            "千杯佳酿需求": result.GetValue("generalawakeinfo.maxnum"),
            "当前已喝": result.GetValue("generalawakeinfo.invalidnum"),
            "满技能": result.GetValue("generalawakeinfo.isfull") == 1,
        }
        return dict_info


@ProtocolMgr.Protocol("至尊觉醒详情", ("generalId",))
async def getAwaken2Info(account: 'Account', result: 'ServerResult', generalId):
    if result.success:
        dict_info = {
            "未觉醒": result.GetValue("generalawakeinfo.isawaken") == 0,
            "每次消耗杜康酒": result.GetValue("generalawakeinfo.dukang"),
            "剩余杜康酒": result.GetValue("generalawakeinfo.remaindukang"),
            "千杯佳酿需求": result.GetValue("generalawakeinfo.maxnum"),
            "当前已喝": result.GetValue("generalawakeinfo.num"),
            "满技能": result.GetValue("generalawakeinfo.isfull") == 1,
        }
        return dict_info


@ProtocolMgr.Protocol("觉醒", ("generalId",))
async def awakenGeneral(account: 'Account', result: 'ServerResult', generalId, general, need_num=0):
    if result.success:
        tips1 = "免费" if need_num == 0 else f"消耗{need_num}觉醒酒"
        tips2 = f"觉醒大将{general['generalname']}"
        if "awakengeneralid" in result.result:
            account.logger.info("%s, %s, 成功觉醒", tips1, tips2)
        else:
            account.logger.info("%s, %s", tips1, tips2)


@ProtocolMgr.Protocol("至尊觉醒", ("generalId",))
async def awakenGeneral2(account: 'Account', result: 'ServerResult', generalId, general, need_num):
    if result.success:
        tips1 = "免费" if need_num == 0 else f"消耗{need_num}杜康酒"
        tips2 = f"至尊觉醒大将{general['generalname']}"
        if "awakengeneralid" in result.result:
            account.logger.info("%s, %s, 成功觉醒", tips1, tips2)
        else:
            account.logger.info("%s, %s", tips1, tips2)


@ProtocolMgr.Protocol("千杯佳酿", ("generalId",))
async def useSpecialLiquor(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        account.logger.info("大将[%s]使用千杯佳酿", general["generalname"])


@ProtocolMgr.Protocol("大将")
async def getAllBigGenerals(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "大将": result.GetValueList("general"),
        }
        return dict_info


@ProtocolMgr.Protocol("大将训练位")
async def getBigTrainInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "经验书": result.GetValue("expbook"),
            "免费次数": result.GetValue("freenum"),
            "等级上限": result.GetValue("maxbglv"),
            "训练位数": result.GetValue("totalpos"),
            "训练位": result.GetValue("traininfo"),
        }
        return dict_info


@ProtocolMgr.Protocol("训练大将", ("trainPosId", "generalId"))
async def startBigTrain(account: 'Account', result: 'ServerResult', trainPosId, generalId, general):
    if result.success:
        account.logger.info("训练大将[%s]", general["name"])


@ProtocolMgr.Protocol("突飞大将", ("generalId",))
async def fastTrainBigGeneral(account: 'Account', result: 'ServerResult', generalId, general, num):
    if result.success:
        account.logger.info("花费%d大将令突飞大将[%s]", num, general["name"])


@ProtocolMgr.Protocol("转生成大将", ("generalId",))
async def toBigGeneral(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        account.logger.info("武将[%s]转生成大将", general["name"])


@ProtocolMgr.Protocol("晋升大将", ("generalId",))
async def bigGeneralChange(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        account.logger.info("大将[%s]晋升为大将军", general["name"])


@ProtocolMgr.Protocol("突破大将", ("generalId",))
async def newTrainBigGeneral(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        account.logger.info("对大将[%s]进行突破", general["name"])


@ProtocolMgr.Protocol("使用经验书", ("generalId",))
async def useExpBook(account: 'Account', result: 'ServerResult', generalId, general):
    if result.success:
        account.logger.info("使用经验书突飞大将[%s]", general["name"])


@ProtocolMgr.Protocol("阵型")
async def formation(account: 'Account', result: 'ServerResult'):
    if result.success:
        formation_id = result.GetValue("formation.formationid")
        if formation_id > 0:
            formation_id //= 20
            return account.user.get_formation_by_id(formation_id)
    return account.user.get_formation_by_id(0)


@ProtocolMgr.Protocol("设置默认阵型", ("formationId",))
async def saveDefaultFormation(account: 'Account', result: 'ServerResult', formationId, formation):
    if result.success:
        account.logger.info("设置默认阵型为%s", formation)


async def doSaveDefaultFormation(account: 'Account', formation: str):
    formation_id = account.user.get_formation_by_name(formation)
    if formation_id > 0:
        formation_id *= 20
        await saveDefaultFormation(account, formationId=formation_id, formation=formation)


@ProtocolMgr.Protocol("大将历练")
async def getGeneralToughenInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        result.GetValue("generalid")
