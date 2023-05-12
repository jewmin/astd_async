import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("炼化")
async def getBaowuPolishInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "炼化机会": result.GetValue("num"),
            "专属玉佩": result.GetValueList("specialtreasure"),
            "家传玉佩": result.GetValueList("baowu"),
        }
        return dict_info


@ProtocolMgr.Protocol("玉佩炼化", ("storeId",))
async def polish(account: 'Account', result: 'ServerResult', storeId, baowu):
    if result.success:
        old_attribute_base = baowu["attribute_base"]
        baowu["polishtimes"] = result.GetValue("baowu.polishtimes")
        baowu["attribute_base"] = result.GetValue("baowu.attribute_base")
        baowu["gold"] = result.GetValue("baowu.gold")
        diff_attribute_base = baowu["attribute_base"] - old_attribute_base
        if diff_attribute_base > 0:
            tips = f"属性+{diff_attribute_base}"
        else:
            tips = "属性无变化"
        account.logger.info("炼化玉佩, %s", tips)
        return True


@ProtocolMgr.Protocol("专属玉佩开光", ("storeId",))
async def consecrateSpecialTreasure(account: 'Account', result: 'ServerResult', storeId, special_treasure):
    if result.success:
        msg = "专属玉佩开光"
        if "additionalattribute" in result.result:
            msg += ", 激活属性"
            special_treasure["additionalattribute"] = {"attribute": []}
            for attribute in result.result["additionalattribute"]:
                special_treasure["additionalattribute"]["attribute"].append(":".join([attribute["attribute"], attribute["name"], attribute["lv"], attribute["value"]]))
                msg += f", {attribute['name']}"
        account.logger.info(msg)


@ProtocolMgr.Protocol("专属玉佩进化", ("storeId",))
async def evolveSpecialTreasure(account: 'Account', result: 'ServerResult', storeId):
    if result.success:
        account.logger.info("专属玉佩进化")


@ProtocolMgr.Protocol("玉佩升级", ("storeId", "storeId2", "type"))
async def upgradeBaowu(account: 'Account', result: 'ServerResult', storeId, storeId2, type, special_treasure, baowu, desc):
    if result.success:
        if result.GetValue("upgraderesult", 0) == 1:
            if "baowu" in result.result:
                account.logger.info("%s升级成功, 统+%s 勇+%s 智+%s", desc, result.GetValue("baowu.succlea", 0), result.GetValue("baowu.succstr", 0), result.GetValue("baowu.succint", 0))
            else:
                account.logger.info("%s升级成功, 统+%s 勇+%s 智+%s", desc, result.GetValue("succlea", 0), result.GetValue("succstr", 0), result.GetValue("succint", 0))
        else:
            account.logger.info("%s升级失败", desc)
        return True
