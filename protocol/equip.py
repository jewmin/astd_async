import manager.ProtocolMgr as ProtocolMgr
import logic.Format as Format
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("装备铸造")
async def getSpecialEquipCastInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dict_info = {
            "免费铸造次数": int(result.result["freetimes"]),
            "铸造消耗金币": int(result.result["firstcost"]),
            "精火铸造消耗金币": int(result.result["secondcost"]),
            "免费神火铸造次数": int(result.result["times"]),
            "总进度": int(result.result["maxprogress"]),
            "当前进度": int(result.result["progress"]),
        }
        account.logger.info("铸造进度: %d/%d, 免费铸造次数: %d", dict_info["当前进度"], dict_info["总进度"], dict_info["免费铸造次数"])
        return dict_info


@ProtocolMgr.Protocol("铸造", ("type",))
async def specialEquipCast(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        special_equip_cast_list = BaseObjectList()  # noqa: F405
        special_equip_cast_list.HandleXml('specialequipcast', result.result["specialequipcast"])
        account.logger.info("%s, 获得%s", kwargs["msg"], ", ".join(special_equip_cast.rewardinfo for special_equip_cast in special_equip_cast_list))


@ProtocolMgr.Protocol("水晶石")
async def getCrystal(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dict_info = {
            "水晶石": result.result["baoshidto"],
        }
        return dict_info


@ProtocolMgr.Protocol("水晶石进阶", ("storeId",))
async def upgradeCrystal(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        baoshidto = kwargs["baoshidto"]
        account.logger.info("水晶石lv.%s[%s(%s)]进阶成功", baoshidto["baoshilevel"], baoshidto["goodsname"], baoshidto["generalname"])
        return True

    account.logger.warning("水晶石进阶报错: %s", result.error)
    return False


@ProtocolMgr.Protocol("水晶石融合", ("storeId", "baoshiId"))
async def meltCrystal(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        baoshidto = kwargs["baoshidto"]
        account.logger.info("水晶石lv.%s[%s(%s)]融合1颗宝石lv.18成功", baoshidto["baoshilevel"], baoshidto["goodsname"], baoshidto["generalname"])
        return True

    account.logger.warning("水晶石融合报错: %s", result.error)
    return False


@ProtocolMgr.Protocol("套装")
async def getUpgradeInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        account.user.magic = int(result.result["magic"])
        account.user.molistone = int(result.result["molistone"])
        account.user.tickets = int(result.result["ticketnumber"])
        account.user.maxtaozhuanglv = int(result.result["taozhuang"]["maxtaozhuanglv"])
        account.user.playerequipdto.HandleXml('playerequipdto', result.result["playerequipdto"])
        account.logger.info("魔力值: %d, 磨砺石: %d, 点券: %s", account.user.magic, account.user.molistone, Format.GetShortReadable(account.user.tickets))
        if kwargs.get("show", False):
            for playerequipdto in account.user.playerequipdto.values():
                account.logger.info(playerequipdto)


@ProtocolMgr.Protocol("套装强化", ("composite", "num"))
async def upgradeMonkeyTao(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        changeinfo = result.result["changeinfo"]
        account.user.tickets = int(changeinfo["remaintickets"])
        kwargs["equipdto"].HandleXml(changeinfo)

        if isinstance(result.result["addinfo"], list):
            addinfo = result.result["addinfo"]
        else:
            addinfo = [result.result["addinfo"]]
        account.logger.info("套装强化, %s倍暴击, %s", result.result.get("baoji", "1"), ", ".join(f"{v['name']+{v['val']}}" for v in addinfo))


@ProtocolMgr.Protocol("套装蓄力", ("composite",))
async def useXuli(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        if "addinfo" in result.result["xuliinfo"]:
            addinfo = result.result["xuliinfo"]["addinfo"]
            account.logger.info("套装蓄力, %s+%s", addinfo["name"], addinfo["val"])
        elif "gethighnum" in result.result["xuliinfo"]:
            account.logger.info("套装蓄力, 高效次数+%s", result.result["xuliinfo"]["gethighnum"])


@ProtocolMgr.Protocol("专属仓库")
async def getAllSpecialEquip(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        equipdto_list = BaseObjectList()  # noqa: F405
        equipdto_list.HandleXml("equipdto", result.result["equipdto"])
        return equipdto_list


@ProtocolMgr.Protocol("熔炼专属", ("specialId", "all"))
async def smeltSpecialEquip(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        equipdto = kwargs["equipdto"]
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("熔炼%s, 获得%s", equipdto, reward_info)


@ProtocolMgr.Protocol("武将装备")
async def getEquip(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        return result.result["general"]


@ProtocolMgr.Protocol("淬炼详情", ("generalId",))
async def getXiZhugeInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dict_info = {
            "免费淬炼次数": int(result.result.get("freenum", 0)),
            "最大属性": int(result.result["maxattr"]),
            "当前属性": result.result["curattr"],
        }
        if isinstance(result.result["newattr"], dict):
            dict_info["新属性"] = result.result["newattr"]
        return dict_info


@ProtocolMgr.Protocol("淬炼", ("storeId",))
async def xiZhuge(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        attrs = map(int, result.result["newattr"].split(","))
        dict_info = {
            "新属性": {"int": attrs[0], "lea": attrs[1], "str": attrs[2]}
        }
        return dict_info


@ProtocolMgr.Protocol("淬炼确认", ("storeId", "type"))
async def xiZhugeConfirm(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        if kwargs["type"] == 1:
            account.logger.info("淬炼成功, 替换属性")
        else:
            account.logger.info("淬炼失败, 保持原样")


@ProtocolMgr.Protocol("套装磨砺", ("composite", "num"))
async def moli(account: 'Account', result: 'ServerResult', kwargs: dict):
    pass


@ProtocolMgr.Protocol("同级合成", ("baoshiId",))
async def updateBaoshiWholeLevel(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        num = result.result["num"]
        baoshilevel = result.result["baoshilevel"]
        numup = result.result["numup"]
        baoshilevelup = result.result["baoshilevelup"]
        account.logger.info("%s宝石lv.%s -> %s宝石lv.%s", num, baoshilevel, numup, baoshilevelup)
