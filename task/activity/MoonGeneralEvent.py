# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class MoonGeneralEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<赏月送礼>"
        self.type = "moongeneralevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getMGEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        finish = True
        for idx, moralinfo in enumerate(info["士气奖励列表"], 1):
            if moralinfo["state"] == 0:
                finish = False
            elif moralinfo["state"] == 1:
                await event.recvMoralReward(self.account, rewardId=idx)

        if not finish and info["送礼免费次数"] > 0:
            await event.eatMoonCake(self.account, name=info["武将"], cost=0)
            return self.immediate
        elif not finish and info["送礼花费金币"] <= self.GetConfig("cakecost") and info["送礼花费金币"] <= self.GetAvailableGold():
            await event.eatMoonCake(self.account, name=info["武将"], cost=info["送礼花费金币"])
            return self.immediate
        elif info["有下一位武将"]:
            await event.nextGeneral(self.account)
            return self.immediate
        elif info["购买轮数花费金币"] <= self.GetConfig("buyroundcost") and info["购买轮数花费金币"] <= self.GetAvailableGold():
            await event.nextGeneral(self.account)
            return self.immediate

        return self.next_half_hour
