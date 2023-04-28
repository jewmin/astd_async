import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("战兽")
async def getInfoList(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "战兽列表": result.GetValueList("warbeastlist.warbeast"),
            "已有战兽": result.GetValueList("warbeast"),
            "精魄": result.GetValue("food1"),
            "高级精魄": result.GetValue("food2"),
        }
        return dict_info


@ProtocolMgr.Protocol("喂养战兽", ("warbeastId", "foodType"))
async def feed(account: 'Account', result: 'ServerResult', warbeastId, foodType):
    if result and result.success:
        warbeast = result.GetValue("warbeast")
        account.logger.info("喂养战兽[%d], 当前进度(%d/%d)", warbeast["warbeastid"], warbeast["exp"], warbeast["upexp"])
        return warbeast


@ProtocolMgr.Protocol("上下阵战兽", ("warbeastId",))
async def standby(account: 'Account', result: 'ServerResult', warbeastId):
    if result and result.success:
        pass


@ProtocolMgr.Protocol("战兽信息", ("warbeastId",))
async def getInfo(account: 'Account', result: 'ServerResult', warbeastId):
    if result and result.success:
        pass
