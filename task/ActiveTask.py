# flake8: noqa
import logic.Format as Format
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *
from model.enum.TaskType import TaskType


class ActiveTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "行动力"

    async def _Exec(self):
        if self.account.user.curactive <= config["active"]["reserve"]:
            return self.next_half_hour

        for v in config["active"]["sort"]:
            active_config = config["active"][v]
            if not active_config["enable"]:
                continue

            if (refresh_time := await getattr(self, v)(active_config)) is not None:
                return refresh_time

        return self.next_half_hour

    async def royalty(self, active_config):
        dict_info = await make.royaltyWeaveInfo2(self.account)
        if dict_info is None:
            return self.next_half_hour

        if dict_info["消耗行动力"] > self.account.user.curactive:
            return self.next_half_hour

        if dict_info["布匹"] < dict_info["布匹上限"]:
            do_high = active_config["do_high"] and dict_info["剩余高效次数"] > 0
            do_tired = active_config["do_tired"] and dict_info["剩余极限次数"] > 0
            finish_task = active_config["finish_task"] and not self.account.user.is_finish_task(TaskType.Weave) and dict_info["剩余极限次数"] > 0
            if do_high or do_tired or finish_task:
                await make.royaltyWeave2(self.account, times=1, active=dict_info["消耗行动力"])
                return self.immediate

        refresh_list = active_config["list"]
        convert_cost = active_config["cost"]
        if dict_info["布匹"] >= active_config["limit"]["limit"]:
            refresh_list = active_config["limit"]["list"]
            convert_cost = active_config["limit"]["cost"]
        has_trader = dict_info["商人"] in refresh_list
        if not has_trader and dict_info["刷新商人费用"] <= active_config["refresh"]:
            await make.refreshRoyaltyWeaveNew(self.account, cost=dict_info["刷新商人费用"])
            return self.immediate

        if has_trader:
            reward = dict_info["换购商品"].get_reward(0)
            if reward is not None:
                for cost in convert_cost:
                    if cost["type"] == reward.type and cost["lv"] == reward.lv and cost["num"] == reward.num:
                        if dict_info["换购消耗布匹"] <= cost["needweavenum"] and dict_info["换购消耗布匹"] <= dict_info["布匹"]:
                            await make.convertRoyaltyWeaveNew2(self.account, need_weave_num=dict_info["换购消耗布匹"])
                        break

    async def refine(self, active_config):
        dict_info = await refine.getRefineInfo(self.account)
        if dict_info is None:
            return self.next_half_hour

        if not dict_info["可精炼工人"]:
            return self.one_minute

        if dict_info["消耗余料"] > dict_info["当前余料"]:
            return

        if dict_info["消耗行动力"] > self.account.user.curactive:
            return self.next_half_hour

        if dict_info["消耗银币"] > self.get_available("copper"):
            await tickets.doGetTicketsReward(self.account, "银币", 1)

        if dict_info["升级单个工人消耗金币"] <= active_config["refresh_refiner"]["per_cost"]:
            dict_info["工人们"] = sorted(dict_info["工人们"], key=lambda value: value["id"], reverse=True)
            sn = ""
            for var in dict_info["工人们"]:
                sn += var["id"]
            if sn in active_config["refresh_refiner"]["list"]:
                index = active_config["refresh_refiner"]["list"][sn]
                await refine.refreshOneRefiner(self.account, refinerOrder=dict_info["工人们"][index]["order"], refiner=dict_info["工人们"][index], cost=dict_info["升级单个工人消耗金币"])
            
            await refine.refine(self.account, copper=dict_info["消耗银币"], active=dict_info["消耗行动力"])
            return self.immediate

        do_high = active_config["do_high"] and dict_info["剩余高效次数"] > 0
        do_tired = active_config["do_tired"] and dict_info["剩余极限次数"] > 0
        finish_task = active_config["finish_task"] and not self.account.user.is_finish_task(TaskType.Refine)
        if do_high or do_tired or finish_task:
            await refine.refine(self.account, copper=dict_info["消耗银币"], active=dict_info["消耗行动力"])
            return self.immediate

    async def refine_bin_tie(self, active_config):
        dict_info = await refine.getRefineBintieFactory(self.account)
        if dict_info is None:
            return self.next_half_hour

        if dict_info["消耗行动力"] > self.account.user.curactive:
            return self.next_half_hour

        if dict_info["消耗银币"] > self.get_available("copper"):
            await tickets.doGetTicketsReward(self.account, "银币", 1)

        war_chariot_info = await warChariot.getWarChariotInfo(self.account)
        if war_chariot_info is None:
            return

        mode = active_config["mode"]
        if war_chariot_info["当前等级"] >= 100:
            mode = 1

        do_high = active_config["do_high"] and dict_info["剩余高效次数"] > 0
        do_tired = active_config["do_tired"] and dict_info["剩余极限次数"] > 0
        finish_task = active_config["finish_task"] and not self.account.user.is_finish_task(TaskType.RefineBintie)
        if do_high or do_tired or finish_task:
            await refine.doRefineBintieFactory(self.account, mode=mode, copper=dict_info["消耗银币"], active=dict_info["消耗行动力"])
            return self.immediate

    async def caravan(self, active_config):
        dict_info = await caravan.getWesternTradeInfo(self.account)
        if dict_info is None:
            return self.next_half_hour

        if dict_info["进入下一站"]:
            await caravan.nextPlace(self.account)

        if "事件" in dict_info:
            await self.handle_event(dict_info)
            return self.immediate

        dict_info["商人们"] = sorted(dict_info["商人们"], key=lambda value: value["active"])
        for trader in dict_info["商人们"]:
            trader_active = trader["active"]
            if trader_active > active_config["limit"]["active"] or trader_active > self.account.user.curactive:
                continue
            cost = trader["cost"].split(":")
            real_cost = int(cost[1])
            if cost[0] == "gold":
                if real_cost <= active_config["limit"]["gold"] and real_cost <= self.get_available("gold"):
                    return await self.do_trade(trader, "金币", real_cost, trader_active)
            elif cost[0] == "copper":
                if real_cost <= active_config["limit"]["copper"]:
                    if real_cost > self.get_available("copper"):
                        await tickets.doGetTicketsReward(self.account, "银币", 1)
                    return await self.do_trade(trader, "银币", real_cost, trader_active)

        if self.account.user.curactive > active_config["limit"]["max_reserve"]:
            for trader in dict_info["商人们"]:
                trader_active = trader["active"]
                if trader_active > self.account.user.curactive:
                    continue
                cost = trader["cost"].split(":")
                real_cost = int(cost[1])
                if cost[0] == "gold":
                    if real_cost <= active_config["limit"]["gold"] and real_cost <= self.get_available("gold"):
                        return await self.do_trade(trader, "金币", real_cost, trader_active)
                elif cost[0] == "copper":
                    if real_cost <= active_config["limit"]["copper"]:
                        if real_cost > self.get_available("copper"):
                            await tickets.doGetTicketsReward(self.account, "银币", 1)
                        return await self.do_trade(trader, "银币", real_cost, trader_active)

    async def do_trade(self, trader, cost_type, cost, trader_active):
        dict_info = await caravan.westernTrade(self.account, tradeId=trader["id"], trader=trader, cost={cost_type: Format.GetShortReadable(cost), "行动力": trader_active})
        await self.handle_event(dict_info)
        return self.immediate

    async def handle_event(self, dict_info):
        if dict_info is None:
            return

        active_config = config["active"]["caravan"]["event"][dict_info["事件"]]
        if dict_info["事件"] == 1:
            is_double = 0
            if not dict_info["可领取状态"]:
                is_double = 1 if dict_info["双倍奖励消耗金币"] <= active_config["double_cost"] and dict_info["双倍奖励消耗金币"] <= self.get_available("gold") else -1
            await caravan.getKingReward(self.account, isdouble=is_double, pos=dict_info["位置"], cost=dict_info["双倍奖励消耗金币"])

        elif dict_info["事件"] == 2:
            for index, status in enumerate(dict_info["可领取状态"]):
                cost = dict_info["消耗金币"][index]
                if status == "1" and cost <= active_config["use_cost"] and cost <= self.get_available("gold"):
                    await caravan.getTraderReward(self.account, isBuy=index + 1, cost=cost)
            await caravan.getTraderReward(self.account, isBuy=-1, cost=0)

        elif dict_info["事件"] == 3:
            is_double = 0
            if dict_info["双倍奖励消耗金币"] <= active_config["double_cost"] and dict_info["双倍奖励消耗金币"] <= self.get_available("gold"):
                is_double = 1
            await caravan.getWesternTradeReward(self.account, isdouble=is_double, cost=dict_info["双倍奖励消耗金币"])
