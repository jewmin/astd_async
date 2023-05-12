import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("科技")
async def getNewTech(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "科技": result.GetValue("technology"),
            "可用宝石": result.GetValue("baoshi18num"),
            "可用镔铁": result.GetValue("bintienum"),
            "可用点券": result.GetValue("ticketsnum"),
        }
        return dict_info


@ProtocolMgr.Protocol("研究科技", ("techId",))
async def researchNewTech(account: 'Account', result: 'ServerResult', techId, tech):
    if result.success:
        account.logger.info("消耗%s%s, 研究科技[%s], 进度+%d", tech["consumenum"], get_tech_consume_name(tech["consumerestype"], tech["techname"], result.GetValue("addprogress")))


def get_tech_consume_name(consume_res_type):
    res_type_name = {
        "bintie": "镔铁",
        "baoshi_18": "宝石lv.18",
        "tickets": "点券",
    }
    return res_type_name.get(consume_res_type, consume_res_type)
