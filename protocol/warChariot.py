import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("战车")
async def getWarChariotInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "当前等级": result.GetValue("equiplevel"),
            "可提升等级": result.GetValue("needtofull"),
            "升级": result.GetValue("islaststrengthenflag", 0) == 1,
            "总进度": result.GetValue("total"),
            "当前进度": result.GetValue("upgradeeffectnum"),
            "普通强化进度": result.GetValue("upgradenum"),
            "库存玉石": result.GetValue("bowlder") // 100,
            "消耗玉石": result.GetValue("needbowlder"),
            "库存兵器": result.GetValue("equipitemnum"),
            "消耗兵器": result.GetValue("needequipitem"),
            "铁锤列表": result.GetValueList("hammer"),
        }
        return dict_info


@ProtocolMgr.Protocol("强化战车", ("chuiziCri",))
async def strengthenWarChariot(account: 'Account', result: 'ServerResult', chuiziCri, tips):
    if result and result.success:
        dict_info = {
            "总进度": result.GetValue("total"),
            "当前进度": result.GetValue("upgradeeffectnum"),
            "使用铁锤": result.GetValue("chuizi", 0) == 1,
            "进度": result.GetValue("isbaoji", 0),
            "余料": result.GetValue("surplus", 0),
        }
        if dict_info["进度"] == 0:
            msg = "战车升级"
        else:
            hammer_tips = "使用铁锤, " if dict_info["使用铁锤"] else ""
            msg = f"{tips}, {hammer_tips}强化战车, 进度+{dict_info['进度']}, {dict_info['当前进度']}/{dict_info['总进度']}, 余料+{dict_info['余料']}"
        account.logger.info(msg)
        return True
