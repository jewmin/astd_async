import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("仓库")
async def openStorehouse(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "使用": result.GetValue("usesize"),
            "总量": result.GetValue("storesize"),
            "物品": result.result["storehousedto"],
        }
        return dict_info


@ProtocolMgr.Protocol("取出物品", ("baoshiLv", "count", "goodsId"))
async def draw(account: 'Account', result: 'ServerResult', baoshiLv, count, goodsId, name):
    if result.success:
        account.logger.info("从临时仓库拿取物品[%s]", name)
