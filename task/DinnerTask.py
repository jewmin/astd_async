# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class DinnerTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "宴会"

    async def _Exec(self):
        if config["dinner"]["enable"]:
            dict_info = await dinner.getAllDinner(self.account)
            if dict_info:
                if dict_info["已加入队伍"]:
                    return self.immediate

                if dict_info["宴会期间"] and dict_info["剩余宴会次数"] > 0:
                    for team in dict_info["宴会队伍"]:
                        if await dinner.joinDinner(self.account, teamId=team["teamid"], creator=team["creator"]):
                            return self.immediate
                    return self.immediate

        return self.next_half_hour
