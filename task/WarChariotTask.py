# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class WarChariotTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "战车强化"

    async def _Exec(self):
        war_chariot_config = config["equip"]["war_chariot"]
        war_drum_config = config["equip"]["war_drum"]
        if war_chariot_config["enable"]:
            dict_info = await warChariot.getWarChariotInfo(self.account)
            if dict_info is None:
                return self.next_half_hour

            if dict_info["当前等级"] >= 100:
                if war_drum_config["enable"]:
                    refine_info = await refine.getRefineInfo(self.account)
                    war_drum_info = await warDrum.getWarDrumInfo(self.account)
                    if war_drum_info is None:
                        return self.next_half_hour

                    if war_drum_info["库存镔铁"] > war_drum_config["save_steelnum"]:
                        has_max_diff_level = war_drum_info["最大等级差"] >= war_drum_config["diff_level"]
                        if war_drum_config["until_double"] or (refine_info["当前余料"] < int(refine_info["余料上限"] * war_drum_config["refine_rate"])):
                            for v in war_drum_config["sort"]:
                                war_drum = war_drum_info["战鼓列表"][v]
                                if war_drum["高效"] is False:
                                    continue
                                if has_max_diff_level and war_drum["当前等级"] >= war_drum_info["最大战鼓等级"]:
                                    continue
                                if self.can_upgrade_war_drum(war_drum, war_drum_info):
                                    await warDrum.strengthenWarDrum(self.account, type=v, steelnum=war_drum["消耗镔铁"], bowldernum=war_drum["消耗玉石"], ticketnum=war_drum["消耗点券"])
                                    return self.immediate

                return self.next_half_hour

            if dict_info["消耗兵器"] > war_chariot_config["equipment_num"]:
                return self.next_day

            if dict_info["消耗兵器"] > dict_info["库存兵器"]:
                if war_chariot_config["auto_exchange_weapon"]:
                    await tickets.doGetTicketsReward(self.account, "无敌将军炮", 10000)
                    return self.immediate
                else:
                    return self.next_half_hour

            if dict_info["消耗玉石"] > dict_info["库存玉石"]:
                if war_chariot_config["auto_exchange_bowlder"]:
                    await tickets.doGetTicketsReward(self.account, "玉石", 10)
                    return self.immediate
                else:
                    return self.next_half_hour

            if war_chariot_config["only_use_hammer"]:
                for hammer in dict_info["铁锤列表"]:
                    num = hammer["num"]
                    cri = hammer["cri"]
                    if num > 0 and cri <= war_chariot_config["hammer_level"]:
                        return self.strengthen_war_chariot(cri, f"花费{dict_info['消耗兵器']}兵器碎片、{dict_info['消耗玉石']}玉石")

            else:
                cri = 0
                for hammer in dict_info["铁锤列表"]:
                    num = hammer["num"]
                    if num > 0:
                        cri = hammer["cri"]
                        break
                return self.strengthen_war_chariot(cri, f"花费{dict_info['消耗兵器']}兵器碎片、{dict_info['消耗玉石']}玉石")

        return self.next_half_hour

    async def strengthen_war_chariot(self, cri, tips):
        if await warChariot.strengthenWarChariot(self.account, chuiziCri=cri, tips=tips):
            return self.immediate
        else:
            return self.next_half_hour

    def can_upgrade_war_drum(self, war_drum, war_drum_info):
        return war_drum["当前等级"] < war_drum_info["最大等级"] and war_drum["消耗镔铁"] <= war_drum_info["库存镔铁"] and war_drum["消耗玉石"] <= war_drum_info["库存玉石"] and war_drum["消耗点券"] <= war_drum_info["库存点券"]
