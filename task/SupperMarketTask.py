# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class SupperMarketTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "集市"

    async def _Exec(self):
        if config["market"]["auto_buy_item"]:
            await market.bargainSupperMarketCommodity(self.account, commodityId=-1)
            supper_market_dto_set, supper_market_special_dto_set, fresh_time, supplement_num = await market.getPlayerSupperMarket(self.account)
            # 排除金币商品
            if config["market"]["withdraw_gold_item"]:
                with_draw_supper_market_dto_set = set()
                for supper_market_dto in supper_market_dto_set:
                    price_type, _ = supper_market_dto.get_price()
                    if price_type == "gold":
                        if (quality := config["market"]["withdraw_gold_item_exclude"].get(supper_market_dto.name)) is not None:
                            if supper_market_dto.quality >= quality:
                                continue
                        await market.offSupperMarketCommodity(self.account, commodityId=supper_market_dto.id, supper_market_dto=supper_market_dto)
                        with_draw_supper_market_dto_set.add(supper_market_dto)
                supper_market_dto_set -= with_draw_supper_market_dto_set

            # 排除还价失败商品
            config_withdraw_discount_fail = config["market"]["withdraw_discount_fail"]
            if config_withdraw_discount_fail["enable"]:
                with_draw_supper_market_dto_set = set()
                for supper_market_dto in supper_market_dto_set:
                    price_type, price = supper_market_dto.get_price()
                    if config_withdraw_discount_fail[price_type] and supper_market_dto.finalprice > price:
                        await market.offSupperMarketCommodity(self.account, commodityId=supper_market_dto.id, supper_market_dto=supper_market_dto)
                        with_draw_supper_market_dto_set.add(supper_market_dto)
                supper_market_dto_set -= with_draw_supper_market_dto_set

            # 购买商品
            with_draw_supper_market_dto_set = set()
            for supper_market_dto in supper_market_dto_set:
                price_type, price = supper_market_dto.get_price()
                if price_type == "copper":
                    if price > self.get_available("copper"):
                        await tickets.doGetTicketsReward(self.account, "银币", 1)
                    await market.buySupperMarketCommodity(self.account, commodityId=supper_market_dto.id, supper_market_dto=supper_market_dto)
                    with_draw_supper_market_dto_set.add(supper_market_dto)
                elif price_type == "gold" and config["market"]["buy_gold_item"]:
                    if self.is_available_and_sub("gold", price):
                        await market.buySupperMarketCommodity(self.account, commodityId=supper_market_dto.id, supper_market_dto=supper_market_dto)
                        with_draw_supper_market_dto_set.add(supper_market_dto)
            supper_market_dto_set -= with_draw_supper_market_dto_set

            # 进货
            if config["market"]["supplement_item"]["enable"]:
                if supplement_num > 0 and len(supper_market_dto_set) <= config["market"]["supplement_item"]["limit"]:
                    await market.supplementSupperMarket(self.account)
                    fresh_time = self.immediate

            # 特贡
            if config["market"]["buy_special_item"]:
                for supper_market_special_dto in supper_market_special_dto_set:
                    if supper_market_special_dto.state == 1:
                        price_type, price = supper_market_special_dto.get_price()
                        if price_type == "copper":
                            if price > self.get_available("copper"):
                                await tickets.doGetTicketsReward(self.account, "银币", 1)
                            await market.buySupperMarketSpecialGoods(self.account, commodityId=supper_market_special_dto.id, supper_market_special_dto=supper_market_special_dto)
                        elif price_type == "gold":
                            if self.is_available_and_sub("gold", price):
                                await market.buySupperMarketSpecialGoods(self.account, commodityId=supper_market_special_dto.id, supper_market_special_dto=supper_market_special_dto)

            if fresh_time is not None:
                return fresh_time

        return self.next_half_hour
