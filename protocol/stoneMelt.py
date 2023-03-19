import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("熔化", ("gold", "meltGold", "magic", "storeId", "type"))
async def melt(account: 'Account', result: 'ServerResult', gold, meltGold, magic, storeId, type, baowu):
    if result and result.success:
        account.logger.info("熔化[%s(统+%s 勇+%s 智+%s)], 获得玉石+%s", baowu["name"], baowu["attribute_lea"], baowu["attribute_str"], baowu["attribute_int"], result.GetValue("gainbowlder", 0))


async def doMelt(account: 'Account', baowu, is_special_treasure=False):
    t = 2 if is_special_treasure else 1
    return await melt(account, gold=0, meltGold=0, magic=account.user.magic, storeId=baowu["storeid"], type=t, baowu=baowu)
