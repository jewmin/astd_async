# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class BoatEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<龙舟>"
        self.type = "boatevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour
        
        info = await event.getBoatEventInfo(self.account, notice=0)
        if info is None:
            return self.next_half_hour

        if info["组队中"] == 1:
            return self.immediate

        if info["阶段"] == 2:
            await event.startBoatComp(self.account)
            return self.immediate

        if info["阶段"] == 3:
            if info["冲刺花费金币"] <= self.GetConfig("gold", 0):
                await event.dashBoatEvent(self.account, cost=info["冲刺花费金币"])
            return self.immediate

        if info["阶段"] == 4:
            if info["奖励状态"] == 0:
                await event.recvBoatEventFinalReward(self.account)
                return self.immediate
            return self.next_half_hour

        if info["剩余次数"] > 0:
            for team in info["队伍列表"]:
                if team["quality"] == info["龙舟品质"]:
                    await event.joinBoatEventTeam(self.account, teamId=team["teamid"])
                    return self.immediate
            if self.GetConfig("create", False):
                await event.creatBoatEventTeam(self.account)
            return self.immediate

        await event.signUpBoatEvent(self.account, signUpId=0)
        return self.immediate
