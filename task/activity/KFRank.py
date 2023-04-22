# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from model.enum.TaskType import TaskType
from protocol import *


class KFRank(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<对战>"
        self.type = "kfrank"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfrank.getMatchDetail(self.account)
        if info is None:
            return self.next_half_hour

        while info["拥有宝箱"] > 0:
            await kfrank.openBox(self.account)
            info["拥有宝箱"] -= 1

        if info["任务"]["state"] == 1:
            await kfrank.recvTaskReward(self.account)

        if info["可领取上届排名奖励"]:
            await kfrank.recvLastReward(self.account)

        task_config = self.GetConfig("task")
        if task_config["enable"]:
            while info["任务"] is not None and info["任务"]["name"] not in task_config["list"]:
                info["任务"] = await kfrank.changeTask(self.account)

        if info["准备状态"]:
            old_formation = await general.formation(self.account)
            new_formation = self.GetConfig("ack_formation") if info["对战可领取宝箱"] else self.GetConfig("def_formation")
            await general.doSaveDefaultFormation(self.account, new_formation)
            await kfrank.syncData(self.account)
            await kfrank.ready(self.account)
            await general.doSaveDefaultFormation(self.account, old_formation)
            return info["下次战斗冷却时间"] // 1000
        elif info["状态"] == 2:
            return self.next_half_hour
        elif info["对战状态"] == 2:
            return self.one_minute
        elif info["对战状态"] == 1:
            return self.immediate * 5
        elif info["花费军令"] > self.GetConfig("limit_token"):
            return self.next_day
        else:
            if info["对战可领取宝箱"] or not self.account.user.is_finish_task(TaskType.KfRank) or (self.GetConfig("def_enable") and info["积分"] > self.GetConfig("def_score")):
                await kfrank.startMatch(self.account, token=info["花费军令"])
                return self.immediate
            else:
                return self.next_half_hour
