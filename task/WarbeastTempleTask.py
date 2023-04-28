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
        war_beast_config = config["equip"]["war_beast"]
        if war_beast_temple_config["enable"]:
            dict_info = await warbeastTemple.getInfo(self.account)
            if dict_info:
                if dict_info["购买1次"] <= war_beast_temple_config["gold"]:
                    await warbeastTemple.buy(self.account, type=1, cost=dict_info["购买1次"])
                    return self.immediate

        if war_beast_config["enable"]:
            dict_info = await warbeast.getInfoList(self.account)
            if dict_info:
                if dict_info["精魄"] > 0:
                    for war_beast in dict_info["已有战兽"]:
                        while war_beast and war_beast["exp"] < war_beast["upexp"] and dict_info["精魄"] > 0:
                            war_beast = await warbeast.feed(self.account, warbeastId=war_beast["warbeastid"], foodType=1)
                            dict_info["精魄"] -= 1

                if dict_info["高级精魄"] > 0:
                    for war_beast in dict_info["已有战兽"]:
                        while war_beast and war_beast["exp"] < war_beast["upexp"] and dict_info["高级精魄"] > 0:
                            war_beast = await warbeast.feed(self.account, warbeastId=war_beast["warbeastid"], foodType=2)
                            dict_info["高级精魄"] -= 1

        return self.next_half_hour
