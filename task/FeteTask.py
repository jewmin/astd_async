# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *
from model.enum.TaskType import TaskType


class FeteTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "祭祀"

    async def _Exec(self):
        if config["fete"]["auto_fete"]:
            fete_gem_task = self.account.user.task.get(TaskType.FeteGem)
            big_fete_task = self.account.user.task.get(TaskType.BigFete)
            if fete_gem_task is not None and fete_gem_task.finishline == 15:
                fete_config = config["fete"]["task15"]
            elif self.account.user.feteevent:
                fete_config = config["fete"]["event"]
            elif big_fete_task is not None and big_fete_task.finishline == 50:
                fete_config = config["fete"]["task50"]
            else:
                fete_config = config["fete"]["common"]

            fete_list, free_all_fete = await fete.fete(self.account)
            for item in fete_list:
                if item.gold <= fete_config.get(item.name, 0) and self.is_available_and_sub("gold", item.gold):
                    await fete.dofete(self.account, feteId=item.id, gold=item.gold, god=item.name)
                    return self.immediate

            if free_all_fete > 0:
                await fete.dofete(self.account, feteId=6, gold=0, god="大祭祀")
                return self.immediate

            if self.account.user.feteevent:
                dict_info = await fete.getFeteEventInfo(self.account)
                if dict_info is not None:
                    for god in dict_info["神"]:
                        if god["state"] == "1":
                            await fete.recvFeteTicket(self.account, feteId=god["godticket"]["id"])

        return self.next_half_hour
