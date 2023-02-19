import manager.ProtocolMgr as ProtocolMgr
import logic.Format as Format

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("宝石矿洞")
async def getPickSpace(account: 'Account', result: 'ServerResult', percent):
    if result.success:
        for v in result.result["playerpickdto"]:
            if float(v["output"]) / float(v["limit"]) >= percent:
                await endBaoshiPick(account, pickSpaceId=v["id"])


async def doGetPickSpace(account: 'Account', percent: float):
    await getPickSpace(account, percent=percent)


@ProtocolMgr.Protocol("采集宝石", ("pickSpaceId",))
async def endBaoshiPick(account: 'Account', result: 'ServerResult', pickSpaceId):
    if result.success:
        account.logger.info("采集宝石, 获得宝石+%s", Format.GetShortReadable(result.result["baoshi"]))
