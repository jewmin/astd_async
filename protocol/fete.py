import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("祭祀活动")
async def getFeteEventInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dict_info = {
            "神": result.result["god"]
        }
        return dict_info


@ProtocolMgr.Protocol("领取祭祀活动奖励", ("feteId",))
async def recvFeteTicket(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        account.logger.info("领取祭祀活动奖励, 获得宝石+%s", result.result["godticket"]["baoshi"])


@ProtocolMgr.Protocol("祭祀神庙", sub_module=False)
async def fete(account: 'Account', result: 'ServerResult', kwargs: dict):
    fete_list = BaseObjectList()  # noqa: F405
    free_all_fete = 0
    if result and result.success:
        fete_list.HandleXml('fete', result.result["fetelist"]["fete"])
        free_all_fete = result.GetValue("fetelist.freeallfete")
    return fete_list, free_all_fete


@ProtocolMgr.Protocol("祭祀", ("feteId",))
async def dofete(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        account.logger.info("花费%d金币祭祀[%s]", kwargs["gold"], kwargs["god"])
        gains = result.GetValueList("gains.gain")
        for gain in gains:
            account.logger.info("%d倍暴击, 获得%s+%d", gain["pro"], gain["addtype"], gain["addvalue"])
