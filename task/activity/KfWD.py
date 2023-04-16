# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class KfWD(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<武斗会>"
        self.type = "showkfwd"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfwd.getSignupList(self.account)
        if info is None:
            return self.next_half_hour

        if info["报名状态"] == 0:
            await kfwd.signUp(self.account)
            return self.immediate
        elif info["报名状态"] == 1:
            if info["冷却时间"] < 0:
                medal_gift = await kfwd.getWdMedalGift(self.account)
                for medal in medal_gift["勋章"]:
                    if medal["cangetreward"] == 1:
                        await kfwd.recvWdMedalGift(self.account, medalId=medal["id"])
                detail = await kfwd.getTributeDetail(self.account)
            else:
                detail = await kfwd.getMatchDetail(self.account)
            if detail is not None:
                if detail["积分奖励"]:
                    await kfwd.getScoreTicketsReward(self.account)
                    return self.immediate
                elif "比赛奖励" in detail:
                    for tribute in detail["比赛奖励"]:
                        if "gold" not in tribute and tribute["state"] == 2:
                            await kfwd.buyTribute(self.account, tribute=tribute)
                            return self.immediate

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            await kfwd.openBoxById(self.account, gold=0)

        return self.next_half_hour
