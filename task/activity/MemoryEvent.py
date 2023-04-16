# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class BoatEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<新春拜年>"
        self.type = "memoryevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await memoryEvent.getMemoryEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        for hongbao in info["红包"]:
            if hongbao["canopen"] == 1:
                if hongbao["num"] > 0:
                    await memoryEvent.openHongbao(self.account, type=hongbao["id"])
                    return self.immediate
                elif hongbao["cost"] <= self.GetConfig("hongbaocost", 0):
                    await memoryEvent.openHongbao(self.account, type=hongbao["id"], gold=hongbao["cost"])
                    return self.immediate

        for picreward in info["回忆图"]:
            if picreward["state"] == 1:
                await memoryEvent.openPicReward(self.account, rewardId=picreward["id"])
                return self.immediate

        if info["拜年免费次数"] > 0:
            await memoryEvent.newYearVisit(self.account)
            return self.immediate
        elif info["拜年花费金币"] <= self.GetConfig("wishcost", 0):
            await memoryEvent.newYearVisit(self.account, gold=info["拜年花费金币"])
            return self.immediate

        return self.next_half_hour
