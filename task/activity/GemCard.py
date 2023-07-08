# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class GemCard(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<宝石翻牌>"
        self.type = "gifteventbaoshi4"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await gemCard.getGemCardInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["免费次数"] > 0:
            cost = 0
            double = 0
            cost_cost = 0
            double_cost = 0
            is_combo, can_combo, combo_id = self.check_combo(info["卡牌"])
            if can_combo:
                if info["升级次数"] < info["免费升级次数"]:
                    for card in info["卡牌"]:
                        if card["id"] == combo_id:
                            card["combo"] += 1
                            is_combo = True
                            break
                elif info["升级花费金币"] <= self.GetConfig("upgradegold") and self.IsAvailableAndSubGold(info["升级花费金币"]):
                    for card in info["卡牌"]:
                        if card["id"] == combo_id:
                            card["combo"] += 1
                            cost_cost = info["升级花费金币"]
                            is_combo = True
                            break
            total = sum([item["combo"] for item in info["卡牌"]])
            if (is_combo and info["组合倍数"] >= self.GetConfig("comboxs") and total >= self.GetConfig("total")) or (info["免费次数"] <= info["免费翻倍次数"]):
                if info["免费翻倍次数"] > 0:
                    double = 1
                elif info["翻倍花费金币"] <= self.GetConfig("doublecost") and self.IsAvailableAndSubGold(info["翻倍花费金币"]):
                    double = 1
                    double_cost = info["翻倍花费金币"]
                else:
                    double = 0
            card_list = ",".join([str(item["combo"]) for item in info["卡牌"]])
            if is_combo:
                total *= 6
            if double == 1:
                total *= 10
            total *= 100
            await gemCard.receiveGem(self.account, cost=cost, doubleCard=double, list=card_list, double_cost=double_cost, cost_cost=cost_cost, baoshi=total)
            return self.immediate
        elif info["购买次数花费金币"] <= self.GetConfig("buygold") and self.IsAvailableAndSubGold(info["购买次数花费金币"]):
            return self.immediate

        return self.next_half_hour

    def check_combo(self, card_list):
        tmp_card_list = sorted(card_list, key=lambda obj: obj["combo"])
        combo = 0
        for card in tmp_card_list:
            combo = combo * 10 + card["combo"]
        if combo in self.GetConfig("combo"):
            return True, False, -1
        else:
            if combo in self.GetConfig("upgrade"):
                return False, True, tmp_card_list[self.GetConfig("upgrade")[combo]]["id"]
            else:
                return False, False, -1
