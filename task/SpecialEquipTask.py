# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class SpecialEquipTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "装备铸造"

    async def _Exec(self):
        special_equip_config = config["equip"]["special_equip"]
        if special_equip_config["enable"]:
            dict_info = await equip.getSpecialEquipCastInfo(self.account)
            if dict_info is not None:
                if dict_info["当前进度"] >= dict_info["总进度"]:
                    if dict_info["免费神火铸造次数"] > 0:
                        await equip.specialEquipCast(self.account, type=3, msg="免费神火铸造")
                    else:
                        await equip.specialEquipCast(self.account, type=2, msg="免费精火铸造")
                    return self.immediate

                if dict_info["免费铸造次数"] > 0:
                    await equip.specialEquipCast(self.account, type=1, msg="免费铸造")
                    return self.immediate

                if dict_info["铸造消耗金币"] <= special_equip_config["firstcost"] and dict_info["铸造消耗金币"] <= self.get_available("gold"):
                    await equip.specialEquipCast(self.account, type=1, msg=f"花费{dict_info['铸造消耗金币']}金币铸造")
                    return self.immediate

                if dict_info["精火铸造消耗金币"] <= special_equip_config["secondcost"] and dict_info["精火铸造消耗金币"] <= self.get_available("gold"):
                    await equip.specialEquipCast(self.account, type=2, msg=f"花费{dict_info['精火铸造消耗金币']}金币精火铸造")
                    return self.immediate

            equipdto_list = await equip.getAllSpecialEquip(self.account)
            if equipdto_list is not None:
                for equipdto in equipdto_list:
                    if equipdto.quality <= special_equip_config["smelt"]["quality"]:
                        await equip.smeltSpecialEquip(self.account, specialId=equipdto.storeid, all=1)
                    elif equipdto.equiplevel <= special_equip_config["smelt"]["level"]:
                        await equip.smeltSpecialEquip(self.account, specialId=equipdto.storeid, all=1)

        return self.next_half_hour
