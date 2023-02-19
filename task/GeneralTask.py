# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class GeneralTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "武将"

    async def _Exec(self):
        dict_info = await general.getRefreshGeneralInfo(self.account)
        if dict_info is not None:
            awaken_generals = []
            awaken_generals2 = [] # 至尊觉醒
            for g in dict_info["武将"]:
                if "generalname" not in g or g["online"] == "1":
                    continue

                if config["general"]["wash"]["enable"] and (dict_info["免费白金洗次数"] > 0 or dict_info["免费至尊洗次数"] > 0):
                    detail = await general.getRefreshGeneralDetailInfo(self.account, generalId=g["generalid"], general=g)
                    if detail is not None:
                        if "新属性" in detail:
                            await self.refresh_general_confirm(g, detail["原始属性"], detail["新属性"])
                            return self.immediate

                        limit_attr = detail["武将等级"] + 20
                        if detail["武将等级"] == 400:
                            limit_attr = self.account.user.playerlevel + 20

                        for v in detail["原始属性"].values():
                            if limit_attr - v > 1:
                                if dict_info["免费白金洗次数"] > 0:
                                    result = await general.refreshGeneral(self.account, generalId=g["generalid"], refreshModel=2)
                                else:
                                    result = await general.refreshGeneral(self.account, generalId=g["generalid"], refreshModel=3)
                                if result is not None:
                                    await self.refresh_general_confirm(g, detail["原始属性"], result["新属性"])
                                return self.immediate

                # isfull maxlevel liquornum freeliquornum needliquornum needbaoshinum isawaken maxnum invalidnum
                if config["general"]["awaken"]["enable"]:
                    if g.get("awaken2", 0) == 1:
                        if g["generalname"] in config["general"]["awaken"]["general2"]:
                            detail = await general.getAwaken2Info(self.account, generalId=g["generalid"])
                            if detail is None:
                                continue
                            if detail["满技能"]:
                                continue
                            awaken_generals2.append((g, detail, config["general"]["awaken"]["general2"][g["generalname"]]))

                    elif "isawaken" in g:
                        if g["generalname"] in config["general"]["awaken"]["general"]:
                            detail = await general.getAwakenGeneralInfo(self.account, generalId=g["generalid"])
                            if detail is None:
                                continue
                            if detail["满技能"]:
                                continue
                            priority = config["general"]["awaken"]["general"][g["generalname"]]
                            if g["isawaken"] == 1:
                                priority += 500
                            awaken_generals.append((g, detail, priority))

            if config["general"]["awaken"]["enable"]:
                awaken_generals2.sort(key=lambda s: s[2])
                awaken_generals.sort(key=lambda s: s[2])
                for g, detail, _ in awaken_generals2:
                    if detail["当前已喝"] >= detail["千杯佳酿需求"]:
                        await general.useSpecialLiquor(self.account, generalId=g["generalid"], general=g)
                        return self.immediate
                    if detail["剩余杜康酒"] >= detail["每次消耗杜康酒"]:
                        await general.awakenGeneral2(self.account, generalId=g["generalid"], general=g, need_num=detail["每次消耗杜康酒"])
                        return self.immediate

                for g, detail, _ in awaken_generals:
                    if detail["当前已喝"] >= detail["千杯佳酿需求"]:
                        await general.useSpecialLiquor(self.account, generalId=g["generalid"], general=g)
                        return self.immediate
                    if detail["免费觉醒酒"] >= detail["需要觉醒酒"]:
                        await general.awakenGeneral(self.account, generalId=g["generalid"], general=g)
                        return self.immediate
                    if general["isawaken"] == 0:
                        if config["general"]["awaken"]["use_stone"] and detail["拥有觉醒酒"] >= detail["需要觉醒酒"]:
                            await general.awakenGeneral(self.account, generalId=g["generalid"], general=g, need_num=detail["需要觉醒酒"])
                            return self.immediate
                        else:
                            break
                    if config["general"]["awaken"]["only_awaken"]:
                        break
                    if config["general"]["awaken"]["use_stone"] and detail["拥有觉醒酒"] >= detail["需要觉醒酒"]:
                        await general.awakenGeneral(self.account, generalId=g["generalid"], general=g, need_num=detail["需要觉醒酒"])
                        return self.immediate

        # techid techname techlevel progress requireprogress consumerestype('bintie','baoshi_18','tickets') consumenum
        if config["general"]["tech"]["enable"]:
            dict_info = await tech.getNewTech(self.account)
            if dict_info is not None:
                upgrade = False
                for t in dict_info["科技"]:
                    if t["techname"] not in config["general"]["tech"]["list"]:
                        continue
                    elif t["techlevel"] >= 5:
                        continue
                    elif t["consumerestype"] == "tickets":
                        if t["consumenum"] > self.get_available("tickets"):
                            continue
                    elif t["consumerestype"] == "bintie":
                        if t["consumenum"] > dict_info["可用镔铁"]:
                            continue
                    elif t["consumerestype"] == "baoshi_18":
                        if t["consumenum"] > dict_info["可用宝石"]:
                            continue
                    await tech.researchNewTech(self.account, techId=t["techid"], tech=t)
                    upgrade = True

                if upgrade:
                    return self.immediate

        # big biglv generalid generallv istop name num
        # pos biglv generalid generaltype change name num
        if config["general"]["big"]["enable"]:
            dict_info = await general.getAllBigGenerals(self.account)
            train_info = await general.getBigTrainInfo(self.account)
            if dict_info is not None and train_info is not None:
                big_config = config["general"]["big"]
                dict_info["待转生大将"] = []
                dict_info["待突破大将"] = []
                dict_info["待突飞大将"] = []
                for i in range(len(dict_info["大将"]) - 1, -1, -1):
                    g = dict_info["大将"][i]
                    if g["big"] == 0:
                        dict_info["待转生大将"].append(g)
                    elif g["num"] > 0:
                        if g["biglv"] == train_info["等级上限"]:
                            dict_info["待突破大将"].append(g)
                        else:
                            dict_info["待突飞大将"].append(g)

                for g in dict_info["待转生大将"]:
                    await general.toBigGeneral(self.account, generalId=g["generalid"], general=g)

                pos = 1
                for g in dict_info["待突破大将"]:
                    await general.startBigTrain(self.account, trainPosId=pos, generalId=g["generalid"], general=g)
                    pos += 1
                    if pos > train_info["训练位数"]:
                        pos = 1
                        await self.train_general(train_info["训练位数"], big_config["new_train"])
                if pos > 1:
                    await self.train_general(pos - 1, big_config["new_train"])

                for g in dict_info["待突飞大将"]:
                    if g["num"] >= big_config["fast_train"]:
                        await general.startBigTrain(self.account, trainPosId=1, generalId=g["generalid"], general=g)
                        while g["num"] >= big_config["fast_train"]:
                            await general.fastTrainBigGeneral(self.account, generalId=g["generalid"], general=g, num=big_config["fast_train"])
                            g["num"] -= big_config["fast_train"]

                dict_info = await general.getAllBigGenerals(self.account)
                for i in range(len(dict_info["大将"]) - 1, -1, -1):
                    g = dict_info["大将"][i]
                    if g["biglv"] == train_info["等级上限"]:
                        dict_info["大将"].remove(g)
                    elif g["quality"] < 200:  # 品质低于200，旧武将，不训练
                        dict_info["大将"].remove(g)
                    else:
                        g["index"] = big_config["dict"].get(g["name"], 9999)
                dict_info["大将"] = sorted(dict_info["大将"], key=lambda obj: obj["index"])
                pos = 1
                for g in dict_info["大将"]:
                    await general.startBigTrain(self.account, trainPosId=pos, generalId=g["generalid"], general=g)
                    pos += 1
                    if pos > train_info["训练位数"]:
                        break

                train_info = await general.getBigTrainInfo(self.account)
                for train in train_info["训练位"]:
                    while train_info["免费次数"] >= big_config["fast_train"]:
                        await general.fastTrainBigGeneral(self.account, generalId=train["generalid"], general=train)
                        train_info["免费次数"] -= big_config["fast_train"]
                    for expbook in train_info["经验书"]:
                        if expbook["type"] == train["generaltype"] and expbook["num"] > 0:
                            await general.useExpBook(self.account, generalId=train["generalid"], general=train)
                            expbook["num"] -= 1

        return self.next_half_hour

    async def refresh_general_confirm(self, g, old_attrs: dict, new_attrs: dict):
        old_total_attr = sum(v for v in old_attrs.values())
        new_total_attr = sum(v for v in new_attrs.values())
        choose = 1 if new_total_attr > old_total_attr else 0
        await general.refreshGeneralConfirm(self.account, generalId=g["generalid"], choose=choose)

    async def train_general(self, num, new_train):
        train_info = await general.getBigTrainInfo(self.account)
        if train_info is None:
            return
        for train in train_info["训练位"]:
            if num > 0:
                num -= 1
                if train["change"] == 0:
                    await general.bigGeneralChange(self.account, generalId=train["generalid"], general=train)
                else:
                    while train["num"] > new_train:
                        await general.newTrainBigGeneral(self.account, generalId=train["generalid"], general=train)
                        train["num"] -= new_train
