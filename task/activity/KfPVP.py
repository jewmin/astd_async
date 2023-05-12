# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class KfPVP(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<英雄帖>"
        self.type = "showkfpvp"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfpvp.getSignupList(self.account)
        if info is None:
            return self.next_half_hour

        if info["报名状态"] == 0:
            await kfpvp.signUp(self.account)
            return self.immediate

        if info["报名状态"] == 1:
            detail = await kfpvp.getMatchDetail(self.account)
            if detail is not None:
                me = detail["攻方"] if detail["攻方"]["playername"] == self.account.user.playername else detail["守方"]
                if detail["可以鼓舞"] and detail["免费鼓舞"] > 0 and me["inspire"]["attack"] == 0 and me["inspire"]["defend"] == 0:
                    await kfpvp.inspire(self.account, count=1)
                    return self.immediate
                elif detail["冷却时间"] > 0:
                    return detail["冷却时间"] // 1000
            elif info["冷却时间"] < 0:
                detail = await kfpvp.getTributeDetail(self.account)
                if detail is not None:
                    self.account.logger.info("英雄帖初始排名: %d, 最终排名: %d", detail["初始排名"], detail["最终排名"])
                    if detail["最终排名奖励"]:
                        await kfpvp.recvRewardById(self.account, rewardId=1)
                        return self.immediate
                    if detail["最终排名前三奖励"]:
                        await kfpvp.recvRewardById(self.account, rewardId=2)
                        return self.immediate
                    if detail["徽章"] == 0:
                        await kfpvp.recvWdMedal(self.account)
                        return self.immediate

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            await kfpvp.openBoxById(self.account, gold=0)

        return self.two_minute
