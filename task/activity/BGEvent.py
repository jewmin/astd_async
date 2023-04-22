# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class BGEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<大宴群雄>"
        self.type = "bgevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getBGEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        for progress_state in info["宴请奖励"]:
            if progress_state["state"] == 1:
                await event.getBanquetReward(self.account, rewardId=progress_state["id"])

        if info["花费金币"] <= self.GetConfig("limit_cost", 0):
            await event.doBGEvent(self.account, cost=info["花费金币"])
            return self.immediate

        return self.next_half_hour
