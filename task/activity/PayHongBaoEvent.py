# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class PayHongBaoEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<充值送红包>"
        self.type = "payhongbaoevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getPayHongbaoEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["共享红包信息"].get('cangetnum', 0) > 0:
            await event.recvShareHongbao(self.account, rewardId=0, playerId=info["共享红包信息"]["playerid"])
            return self.immediate

        return self.next_half_hour
