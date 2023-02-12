# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *
from model.enum.TaskType import TaskType


class ImposeTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "征收"

    async def _Exec(self):
        if config["impose"]["auto_impose"]:
            impose_num, force_impose_cost = await mainCity.perImpose(self.account)
            imposedto = self.account.user.imposedto
            if imposedto.cdflag and imposedto.lastimposetime > 0:
                return imposedto.lastimposetime

            if impose_num > config["impose"]["reserve"]:
                await mainCity.impose(self.account)
                return self.immediate

            if force_impose_cost <= config["impose"]["force"] and force_impose_cost <= self.get_available("gold"):
                await mainCity.forceImpose(self.account)
                return self.immediate

            if config["impose"]["finish_task"]:
                if not self.account.user.is_finish_task(TaskType.ForceImpose) and force_impose_cost <= self.get_available("gold"):
                    await mainCity.forceImpose(self.account)
                    return self.immediate

                if not self.account.user.is_finish_task(TaskType.Impose):
                    if impose_num > 0:
                        await mainCity.impose(self.account)
                        return self.immediate

                    if force_impose_cost <= self.get_available("gold"):
                        await mainCity.forceImpose(self.account)
                        return self.immediate

        return self.next_half_hour
