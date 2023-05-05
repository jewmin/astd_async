# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class DuanWuEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<百家宴>"
        self.type = "duanwuevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await event.getDuanwuEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        for reward in info["奖励"]:
            if reward["state"] == 1:
                await event.getRewardById(self.account, rewardId=reward["id"], dbId=self.get_choice(reward["choice"]))

        if info["轮数"] > 0:
            if info["饥饿"] > 0:
                if info["普通粽子"] <= self.GetConfig("limit_hunger"):
                    await event.eatZongzi(self.account, gold=0, cost=0)
                    return self.immediate
                elif info["花费金币"] <= self.GetConfig("gold_hunger") and info["花费金币"] <= self.GetAvailableGold():
                    await event.eatZongzi(self.account, gold=1, cost=info["花费金币"])
                    return self.immediate
                else:
                    await event.eatZongzi(self.account, gold=0, cost=0)
                    return self.immediate
            else:
                await event.nextRound(self.account)
                return self.immediate
        elif info["购买轮数花费金币"] <= self.GetConfig("gold_round") and info["购买轮数花费金币"] <= self.GetAvailableGold():
            await event.buyRound(self.account, cost=info["购买轮数花费金币"])
            return self.immediate

        return self.next_half_hour

    def get_choice(self, choice):
        for v in choice:
            if v["bigginfo"]["name"] in self.GetConfig("general"):
                return v["rewardid"]
        return choice[0]["rewardid"]
