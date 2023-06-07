# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *
from functools import cmp_to_key


class GoldGiftType(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<盛宴活动>"
        self.type = "goldgifttype"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        nation = self.account.user.nation
        def helper(x, y):
            key = {
                1: "weinum",
                2: "shunum",
                3: "wunum",
            }
            xx, yy = x[key[nation]], y[key[nation]]
            if x["bufnum"] > y["bufnum"]:
                return -1
            elif x["bufnum"] < y["bufnum"]:
                return 1
            elif xx > yy:
                return -1
            elif xx < yy:
                return 1
            elif x["finishnum"] > y["finishnum"]:
                return -1
            elif x["finishnum"] < y["finishnum"]:
                return 1
            else:
                return 0

        info = await kfBanquet.kfBanquet(self.account)
        if info is not None:
            if info["基础点券"] > 0:
                await kfBanquet.choosenDouble(self.account, type=0, tickets=info["基础点券"])
                return self.immediate
            elif info["所在房间"] > 0:
                return self.immediate * 5
            elif info["状态"] == 1:
                if info["加入盛宴免费次数"] > 0:
                    info["盛宴房间"] = sorted(info["盛宴房间"], key=cmp_to_key(helper))
                    for room in info["盛宴房间"]:
                        if room["nation"] == self.account.user.nation:
                            await kfBanquet.joinBanquet(self.account, room=room["rank"], playername=room["playername"])
                            return self.immediate
                elif info["加入盛宴花费金币"] <= self.GetConfig("buyjoingold") and info["加入盛宴花费金币"] <= self.GetAvailableGold():
                    await kfBanquet.buyBanquetNum(self.account, num=1, cost=info["加入盛宴花费金币"])
                    return self.immediate

        return self.next_half_hour
