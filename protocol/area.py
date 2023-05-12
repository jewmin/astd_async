import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("查看城区", ("areaId", "scopeId"))
async def getAllCity(account: 'Account', result: 'ServerResult', areaId, scopeId):
    if result.success:
        return result.GetValueList("city")
