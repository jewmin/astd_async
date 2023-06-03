# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class GoldGiftType(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<盛宴活动>"
        self.type = "goldgifttype"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfBanquet.kfBanquet(self.account)
        if info is not None:
            if info["基础点券"] > 0:
                await kfBanquet.choosenDouble(self.account, type=0, tickets=info["基础点券"])
                return self.immediate
            elif info["所在房间"] > 0:
                return self.immediate * 5
            elif info["状态"] == 1:
                if info["加入盛宴免费次数"] > 0:
                    for room in info["盛宴房间"]:
                        if room["bufnum"] > 0 and room["nation"] == self.account.user.nation:
                            await kfBanquet.joinBanquet(self.account, room=room["rank"], playername=room["playername"])
                            return self.immediate
                elif info["加入盛宴花费金币"] <= self.GetConfig("buyjoingold") and info["加入盛宴花费金币"] <= self.GetAvailableGold():
                    await kfBanquet.buyBanquetNum(self.account, num=1, cost=info["加入盛宴花费金币"])
                    return self.immediate

        return self.next_half_hour
