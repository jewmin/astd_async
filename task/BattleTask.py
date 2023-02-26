# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class BattleTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "征战"
        self.all_teams = []

    async def Init(self):
        if config["battle"]["enable"]:
            for power_id in config["battle"]["powerid"]:
                while True:
                    army_list = await battle.getPowerInfo(self.account, powerId=power_id)
                    if army_list and "军团" in army_list[-1]["armyname"]:
                        if not army_list[-1]["complete"]:
                            self.all_teams.append(army_list[-1]["armyid"])
                        power_id += 1
                    else:
                        break

    async def _Exec(self):
        if config["battle"]["enable"]:
            dict_info = await battle.battle(self.account)
            if dict_info is None:
                return self.next_half_hour

            if dict_info["免费强攻令"] > 0 and config["battle"]["armyid"] > 0:
                while dict_info["免费强攻令"] > 0:
                    await battle.forceBattleArmy(self.account, armyId=config["battle"]["armyid"])
                    dict_info["免费强攻令"] -= 1
                return self.immediate

            state = dict_info["征战事件"].get("state", "0")
            if state == "1":
                process = list(map(int, dict_info["征战事件"]["process"].split("/")))
                while process[0] < process[1]:
                    await battle.doBattleEvent(self.account)
                    process[0] += 1
                return self.immediate

            elif state == "2":
                await battle.recvBattleEventReward(self.account)
                return self.immediate

            if config["battle"]["auto"]["enable"]:
                if self.account.user.tokencd > 0:
                    return self.account.user.tokencd // 1000
                
                await battle.battleArmy(config["battle"]["auto"]["armyid"])
                return self.immediate

            for armies_id in self.all_teams:
                teamid = await multiBattle.getTeamInfo(self.account, armiesId=armies_id)
                if teamid:
                    return self.next_half_hour

        return self.ten_minute
