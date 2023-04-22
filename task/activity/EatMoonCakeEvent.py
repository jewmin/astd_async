# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class EatMoonCakeEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<中秋月饼>"
        self.type = "eatmooncaketevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await eatMooncakeEvent.getInfo(self.account)
        if info is None:
            return self.next_half_hour

        for eat_state in info["吃货状态"]:
            if eat_state["state"] == 1:
                await eatMooncakeEvent.getProgressReward(self.account, rewardId=eat_state["id"])

        if info["吃蛋黄月饼花费金币"] <= self.GetConfig("gold"):
            await eatMooncakeEvent.eatMooncake(self.account, type=1, cost=info["吃蛋黄月饼花费金币"])
            return self.immediate
        elif info["吃豆沙月饼花费金币"] <= self.GetConfig("gold"):
            await eatMooncakeEvent.eatMooncake(self.account, type=2, cost=info["吃豆沙月饼花费金币"])
            return self.immediate

        return self.next_half_hour
