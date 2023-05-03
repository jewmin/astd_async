# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class QingMingEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<群雄煮酒>"
        self.type = "qingmingevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getQingmingInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["大奖"]:
            await event.getQingmingBigReward(self.account)
            return self.immediate

        if info["轮数"] > 0:
            idx = 0
            for general in info["武将"]:
                if general["state"] == 1:
                    idx += 1
                else:
                    break
            info["酒"] = sorted(info["酒"], key=lambda obj: obj["winenum"], reverse=True)
            for wine in info["酒"]:
                wine_num = wine["winenum"]
                if wine_num + info["醉意"] <= self.GetConfig("drink")[idx]:
                    await event.qingmingDrink(self.account, wineId=wine["id"], gold=0)
                    return self.immediate

                if wine_num == 40 and info["酒仙附体花费金币"] <= self.GetConfig("golddrinkcost") and info["酒仙附体花费金币"] <= self.GetAvailableGold():
                    await event.qingmingDrink(self.account, wineId=wine["id"], gold=1, cost=info["酒仙附体花费金币"])
                    return self.immediate

            if info["酒"][2]["winenum"] + info["醉意"] >= info["最大醉意"]:
                await event.qingmingDrink(self.account, wineId=info["酒"][0]["id"], gold=0)
            else:
                await event.qingmingDrink(self.account, wineId=info["酒"][2]["id"], gold=0)
            return self.immediate

        if info["购买轮数花费金币"] <= self.GetConfig("buycost") and info["购买轮数花费金币"] <= self.GetAvailableGold():
            await event.buyQingmingRound(self.account, cost=info["购买轮数花费金币"])
            return self.immediate

        return self.next_half_hour
