# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class WarbeastTempleTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "战兽圣殿"

    async def _Exec(self):
        war_beast_temple_config = config["equip"]["war_beast_temple"]
        if war_beast_temple_config["enable"]:
            dict_info = await warbeastTemple.getInfo(self.account)
            if dict_info:
                if dict_info["购买1次"] <= war_beast_temple_config["gold"]:
                    await warbeastTemple.buy(self.account, type=1, cost=dict_info["购买1次"])
                    return self.immediate

        return self.next_half_hour
