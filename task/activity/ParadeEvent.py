# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class ParadeEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<阅兵庆典>"
        self.type = "paradeevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await paradeEvent.getParadeEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        for parade_state in info["奖励"]:
            if parade_state["state"] == 1:
                await paradeEvent.getParadeReward(self.account, rewardId=parade_state["id"])

        if info["免费阅兵轮数"] <= 0:
            if info["购买轮数花费金币"] <= self.GetConfig("round_cost") and info["购买轮数花费金币"] <= self.GetAvailableGold():
                await paradeEvent.addRoundTimes(self.account, cost=info["购买轮数花费金币"])
                return self.immediate
            else:
                return self.next_half_hour

        while info["免费阅兵次数"] > 0:
            info["免费阅兵次数"] -= 1
            await paradeEvent.paradeArmy(self.account, cost=0)
        await paradeEvent.getNextGeneral(self.account)

        return self.immediate
