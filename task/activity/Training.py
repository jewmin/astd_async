# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class Training(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<大练兵>"
        self.type = "trainingevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await training.getInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["状态"] == 0:
            await training.start(self.account)
            return self.immediate

        if info["第几轮"] > 0:
            army_idx = -1
            max_army = -1
            for idx, army in enumerate(info["部队"], 1):
                if army > max_army:
                    army_idx = idx
                    max_army = army
            await training.attackArmy(self.account, army=army_idx, army_name=max_army)
            return self.immediate

        for idx, hongbao in enumerate(info["战旗"], 1):
            if hongbao == 1:
                await training.recHongbao(self.account, hongbao=idx)

        hongbao = 0
        while info["红包"] > 0:
            if hongbao >= 3 and info["免费重置奖励次数"] > 0:
                await training.resetReward(self.account)
                return self.immediate

            await training.getReward(self.account)
            info["红包"] -= 1
            hongbao += 1

        return self.next_half_hour
