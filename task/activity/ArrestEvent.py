# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class ArrestEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<抓捕>"
        self.type = "arrestevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getArrestEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["可领取抓捕令"] == 1:
            await event.recvArrestToken(self.account)
            return self.immediate

        if info["俘虏"] > 0:
            if info["免费鞭子次数"] > 0:
                await event.shenSlaves(self.account, cost=0, highLv=1)
            elif info["鞭子花费金币"] <= self.GetConfig("high_gold", 0) and self.IsAvailableAndSubGold(info["鞭子花费金币"]):
                await event.shenSlaves(self.account, cost=info["鞭子花费金币"], highLv=1)
            else:
                await event.shenSlaves(self.account, cost=0, highLv=0)
            return self.immediate

        if info["粽子数量"] > 0:
            await event.eatRiceDumpling(self.account)
            return self.immediate

        if info["抓捕令"] == 0 and info["购买抓捕令花费金币"] <= self.GetConfig("buy_gold", 0) and self.IsAvailableAndSubGold(info["购买抓捕令花费金币"]):
            await event.buyArrestToken(self.account, cost=info["购买抓捕令花费金币"])
            return self.immediate

        return self.next_half_hour
