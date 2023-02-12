# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class EquipTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "强化"

    async def _Exec(self):
        monkey_config = config["equip"]["monkey"]
        if monkey_config["enable"]:
            await equip.getUpgradeInfo(self.account, show=True)
            upgrade = False
            for composite, equipdto in self.account.user.playerequipdto.items():
                if equipdto.xuli >= equipdto.maxxuli:
                    await equip.useXuli(self.account, composite=composite)

                if equipdto.monkeylv >= self.account.user.maxtaozhuanglv:
                    continue

                if equipdto.monkeylv >= 15 and equipdto.powertao == 0:
                    continue

                if equipdto.tickets <= monkey_config["use_tickets"] and equipdto.tickets <= self.get_available("tickets"):
                    await equip.upgradeMonkeyTao(self.account, composite=composite, num=40, equipdto=equipdto)
                    upgrade = True

            if upgrade:
                return self.immediate

        zhuge_config = config["equip"]["zhuge"]
        if zhuge_config["enable"]:
            generals = await equip.getEquip(self.account)
            if generals is not None:
                upgrade = False
                for general in generals:
                    if general.get("zhugeid", "0") == "0":
                        continue

                    detail = await equip.getXiZhugeInfo(self.account, generalId=general["generalid"])
                    if detail is None:
                        continue

                    if "新属性" in detail:
                        await equip.xiZhugeConfirm(self.account, storeId=general["zhugeid"], type=self.check_attr(detail["当前属性"], detail["新属性"]))
                        upgrade = True
                        continue

                    if detail["免费淬炼次数"] <= 0:
                        continue

                    for attr in detail["当前属性"].values():
                        if int(attr) < detail["最大属性"]:
                            result = await equip.xiZhuge(self.account, storeId=general["zhugeid"])
                            if result is not None:
                                await equip.xiZhugeConfirm(self.account, storeId=general["zhugeid"], type=self.check_attr(detail["当前属性"], result["新属性"]))
                            upgrade = True

                if upgrade:
                    return self.immediate

        goods_config = config["equip"]["goods"]
        if goods_config["enable"]:
            dict_info = await goods.openStorehouse(self.account)
            if dict_info is not None:
                for storehousedto in dict_info["物品"]:
                    if dict_info["使用"] < dict_info["总量"]:
                        if int(storehousedto.get("remaintime", 0)) > 0:
                            name = storehousedto.get("equipname", storehousedto.get("name", ""))
                            await goods.draw(self.account, baoshiLv=0, count=1, goodsId=storehousedto["id"], name=name)
                            dict_info["使用"] += 1
                    else:
                        break

        crystal_config = config["equip"]["crystal"]
        if crystal_config["enable"]:
            dict_info = await equip.getCrystal(self.account)
            if dict_info is not None:
                upgrade = False
                for baoshidto in dict_info["水晶石"]:
                    if baoshidto.get("istop", "0") == "1":
                        continue

                    curbaoshinum = int(baoshidto.get("curbaoshinum", "0"))
                    totalbaoshinum = int(baoshidto.get("totalbaoshinum", "0"))
                    if totalbaoshinum == 0:
                        continue

                    if totalbaoshinum <= curbaoshinum:
                        if not await equip.upgradeCrystal(self.account, storeId=baoshidto["storeid"], baoshidto=baoshidto):
                            return self.next_half_hour
                        else:
                            upgrade = True

                    elif int(baoshidto["baoshilevel"]) >= crystal_config["level"]:
                        if not await equip.meltCrystal(self.account, storeId=baoshidto["storeid"], baoshiId=18, baoshidto=baoshidto):
                            return self.next_half_hour
                        else:
                            upgrade = True

                if upgrade:
                    return self.immediate

        merge_config = config["equip"]["merge"]
        if merge_config["enable"]:
            for level in range(1, merge_config["level"]):
                if not await equip.updateBaoshiWholeLevel(self.account, baoshiId=level):
                    break

        return self.ten_minute

    def check_attr(self, old_attrs, new_attrs):
        old_attr = 0
        new_attr = 0
        for value in old_attrs.values():
            old_attr += int(value)
        for value in new_attrs.values():
            new_attr += int(value)
        if new_attr > old_attr:
            return 1
        return 2
