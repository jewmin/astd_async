# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class TowerStage(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<宝塔活动>"
        self.type = "towerstage"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour
        
        info = await festaval.getTowerEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["阶段"] == 1 and info["选中宝塔"] == 0:
            await festaval.doAcceptByTowerId(self.account, tower=info["宝塔"][self.GetConfig("tower")])
        elif info["阶段"] == 2 and info["状态"] == 0 and info["宝石"] >= info["宝塔"]["baoshi"]:
            await festaval.finishTower(self.account)

        return self.next_half_hour
