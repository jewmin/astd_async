import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("群雄争霸")
async def getMatchDetail(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "攻方": result.GetValue("message.attacker"),
            "守方": result.GetValue("message.defender"),
            "可以鼓舞": result.GetValue("message.canbuymorereward"),
            "鼓舞花费金币": result.GetValue("message.buymorerewardgold", 0),
        }
        return info


@ProtocolMgr.Protocol("支持", ("competitorId",))
async def support(account: 'Account', result: 'ServerResult', competitorId, playername, cost=0):
    if result.success:
        account.logger.info("花费%d金币, 支持[%s]", cost, playername)


@ProtocolMgr.Protocol("争霸商城")
async def getKfzbMarket(account: 'Account', result: 'ServerResult'):
    if result.success:
        goods = {
            "冷却时间": result.GetValue("message.nextcd"),
            "商品": result.GetValueList("message.kfzbshop"),
        }
        return goods


@ProtocolMgr.Protocol("购买商品", ("marketId",))
async def buyFromKfzbMarket(account: 'Account', result: 'ServerResult', marketId):
    if result.success:
        pass
