import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
from logic.Config import config

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("集市")
async def getPlayerSupperMarket(account: 'Account', result: 'ServerResult', kwargs: dict):
    supper_market_dto_list = BaseObjectList()  # noqa: F405
    supper_market_special_dto_list = BaseObjectList()  # noqa: F405
    fresh_time = None
    supplement_num = 0
    if result.success:
        fresh_time = int(result.result["freshtime"])
        supplement_num = int(result.result["supplementnum"])
        if "suppermarketdto" in result.result:
            supper_market_dto_list.HandleXml("suppermarketdto", result.result["suppermarketdto"])
        if "special" in result.result:
            supper_market_special_dto_list.HandleXml("suppermarketspecialdto", result.result["special"])
        if "giftdto" in result.result:
            await doRecvSupperMarketGift(account, SupperMarketDto(result.result["giftdto"]))  # noqa: F405

    return supper_market_dto_list, supper_market_special_dto_list, fresh_time, supplement_num


@ProtocolMgr.Protocol("商品还价", ("commodityId",))
async def bargainSupperMarketCommodity(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("商品还价")


@ProtocolMgr.Protocol("下架商品", ("commodityId",))
async def offSupperMarketCommodity(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("下架商品: %s", kwargs["supper_market_dto"])


@ProtocolMgr.Protocol("购买商品", ("commodityId",))
async def buySupperMarketCommodity(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("购买商品: %s", kwargs["supper_market_dto"])
        if "giftdto" in result.result:
            await doRecvSupperMarketGift(account, SupperMarketDto(result.result["giftdto"]))  # noqa: F405


@ProtocolMgr.Protocol("购买每日特供", ("commodityId",))
async def buySupperMarketSpecialGoods(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("购买每日特供, 获得%s", kwargs["supper_market_special_dto"])


@ProtocolMgr.Protocol("使用进货令")
async def supplementSupperMarket(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("使用进货令")


@ProtocolMgr.Protocol("放弃赠送商品")
async def abandonSupperMarketGift(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("放弃赠送商品[%s]", kwargs["name"])


@ProtocolMgr.Protocol("领取赠送商品")
async def recvSupperMarketGift(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        if "num" in result.result:
            account.logger.info("领取赠送商品, 获得%s+%s", result.result["name"], result.result["num"])
        else:
            account.logger.info("使用赠送商品[%s]", result.result["name"])


async def doRecvSupperMarketGift(account: 'Account', supper_market_dto: SupperMarketDto):  # noqa: F405
    if config["market"]["gift"]["enable"]:
        if supper_market_dto.name in config["market"]["gift"]["list"]:
            return await recvSupperMarketGift(account)

    await abandonSupperMarketGift(account)


@ProtocolMgr.Protocol("委派商人")
async def getPlayerMerchant(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        if result.result["free"] == "1":
            await trade(account, result.result["merchant"][0])


@ProtocolMgr.Protocol("委派", ("gold", "merchantId"))
async def trade(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        await confirm(account, tradeSN=result.result["tradesn"], merchandise=result.result["merchandise"])


@ProtocolMgr.Protocol("卖出委派商品", ("tradeSN",))
async def confirm(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("卖出委派商品[%s], 获得银币+%s", kwargs["merchandise"], result.result["cost"])
