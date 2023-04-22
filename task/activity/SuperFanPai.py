# flake8: noqa
import random
from task.activity.ActivityTask import ActivityTask
from protocol import *


class SuperFanPai(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<超级翻牌>"
        self.type = "superfanpai"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await superFanpai.getSuperFanpaiInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["翻牌"]:
            await superFanpai.fanOne(self.account, cardId=random.randint(1, 3))
            return self.immediate

        tips = ["卡牌:"]
        tips.extend(f"宝石lv.{card['gemlevel']}+{card['gemnumber']}" for card in info["卡牌"])
        self.info(" ".join(tips))

        if info["翻牌次数"] > 0:
            buy_all = False
            info["卡牌"] = sorted(info["卡牌"], key=lambda obj: obj["gemlevel"])
            if info["卡牌"][0]["gemlevel"] >= self.GetConfig("superlv"):
                buy_all = True
            if buy_all and info["卡牌全开花费金币"] <= self.GetConfig("buyall") and info["卡牌全开花费金币"] <= self.GetAvailableGold():
                await superFanpai.getAll(self.account, cost=info["卡牌全开花费金币"])
                return self.immediate
            else:
                await superFanpai.xiPai(self.account)
                await superFanpai.fanOne(self.account, cardId=info["卡牌"][-1]["id"])
                return self.immediate
        elif info["购买次数花费金币"] <= self.GetConfig("buyone") and info["购买次数花费金币"] <= self.GetAvailableGold():
            await superFanpai.buyTimes(self.account, cost=info["购买次数花费金币"])
            return self.immediate

        return self.next_half_hour
