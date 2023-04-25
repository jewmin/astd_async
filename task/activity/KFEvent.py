# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class KFEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<武斗庆典>"
        self.type = "kfwdeventreward"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfEvent.getKfwdEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["奖励"] > 0:
            await kfEvent.getKfwdReward(self.account)

        return self.next_half_hour
