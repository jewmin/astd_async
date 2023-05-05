# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class WorldTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "世界"

    async def _Exec(self):
        # 领取攻击令
        apply_att_token_config = config["world"]["apply_att_token"]
        if apply_att_token_config["enable"] and float(self.account.user.atttoken) / float(self.account.user.maxattacktoken) <= apply_att_token_config["proportion"]:
            await world.getTranferInfo(self.account)

        # 国家宝箱
        treasure_config = config["world"]["treasure"]
        if treasure_config["enable"] and float(self.account.user.atttoken) / float(self.account.user.maxattacktoken) <= treasure_config["proportion"]:
            treasurenum = await world.getNewAreaTreasureInfo(self.account)
            while treasurenum > treasure_config["reserve"]:
                await world.draw5NewAreaTreasure(self.account)
                treasurenum -= 5

        # 屠城嘉奖
        tu_city_config = config["world"]["tu_city"]
        if tu_city_config["enable"]:
            await world.getTuCityInfo(self.account)

        # 战绩
        score_config = config["world"]["score"]
        if score_config["enable"]:
            ranking_info = await world.getBattleRankingInfo(self.account)
            if ranking_info:
                if ranking_info["上轮战绩排名奖励"] and not ranking_info["已领取上轮战绩排名奖励"]:
                    await world.getBattleRankReward(self.account)
                # 战绩宝箱
                while ranking_info["宝箱"] > 0:
                    await world.openScoreBox(self.account)
                    ranking_info["宝箱"] -= 1
                # 战绩奖励
                for rinfo in ranking_info["战绩奖励"]:
                    if rinfo["canget"] and not rinfo["get"]:
                        await world.getBattleScoreReward(self.account, pos=rinfo["id"])

        # 攻坚战
        nation_task_config = config["world"]["nation_task"]
        if nation_task_config["enable"]:
            nation_task_info = await nation.getNationTaskNewInfo(self.account)
            if nation_task_info:
                if nation_task_info["状态"] == 3:
                    await nation.getNationTaskNewReward(self.account)

        # 决斗
        await self.do_duel()

        # 悬赏
        city_event_config = config["world"]["city_event"]
        if city_event_config["enable"]:
            event_info = await world.getNewCityEventInfo(self.account)
            if event_info:
                # 悬赏星数奖励
                for pos, star_reward in enumerate(event_info["悬赏星数奖励"], 1):
                    if star_reward["state"] == 1:
                        await world.recvNewCityEventStarReward(self.account, pos=pos)
                # 悬赏任务奖励
                if event_info["悬赏已完成"] and event_info["悬赏剩余时间"] == 0:
                    await world.deliverNewCityEvent(self.account)

        area_info = await world.getNewArea(self.account)
        await world.getNewAreaToken(self.account)

        # 设置地图障碍
        area_map = self.account.user.area_map
        for (y, x), a_area in area_info["所有城池"].items():
            if a_area["areaname"] in ("许都", "成都", "武昌"):  # 主城
                area_map[y][x] = 0
            elif "tucitycd" in a_area and a_area["tucitynation"] == self.account.user.nation:  # 屠城
                area_map[y][x] = 1
            elif area_info["穿越"]:  # 穿越
                area_map[y][x] = 1
            elif event_info["悬赏剩余时间"] > 0:  # 悬赏
                area_map[y][x] = 1
            elif a_area["nation"] == self.account.user.nation:  # 本国
                area_map[y][x] = 1
            else:
                area_map[y][x] = 0

        # 城防恢复
        if (cityhprecovercd := area_info["城防恢复cd"]) > 0:
            self.logger.info("等待城防恢复时间: %s", self.account.time_mgr.GetDatetimeString(cityhprecovercd))
            return cityhprecovercd // 1000

        # 封地奖励
        fengdi_config = config["world"]["fengdi"]
        if fengdi_config["enable"]:
            fengdi = self.account.user.fengdi
            if fengdi.finish:
                await world.recvFengdiReward(self.account)
            elif fengdi.nextcd == 0 and fengdi.remainnum > 0:
                if self.account.user.areaid in area_info["封地城池"]:
                    await world.generateBigG(self.account, areaId=self.account.user.areaid)
                elif len(area_info["封地城池"]) > 0:
                    for area_id, a_area in area_info["封地城池"].items():
                        if a_area["fengdicd"] >= fengdi_config["cd"]:
                            next_area = await self.get_next_move_area(area_id, area_info)
                            if next_area is not None:
                                await world.transferInNewArea(self.account, areaId=area_id, area=next_area)
                                return self.immediate
            elif fengdi.nextcd > 0:
                return fengdi.nextcd // 1000

        # 逃跑
        if self.account.user.arreststate == 100:
            cd = await jail.escape(self.account)
            if cd:
                self.logger.info("等待逃跑冷却时间: %s", self.account.time_mgr.GetDatetimeString(cd * 1000))
                return cd

        # 冷却时间
        if self.account.user.tokencdflag and (tokencd := self.account.user.tokencd) > 0:
            self.logger.info("等待军令冷却时间: %s", self.account.time_mgr.GetDatetimeString(tokencd))
            return tokencd // 1000

        # 攻击令
        attack_config = config["world"]["attack"]
        if self.account.user.atttoken > 0:
            # 个人令
            use_token_config = config["world"]["use_token"]
            if use_token_config["enable"]:
                for token in self.account.user.tokenlist:
                    if token.tokenid in use_token_config["list"]:
                        await world.useToken(self.account, token)

            # 不在都城
            if attack_config["main_city"][self.account.user.nation] != self.account.user.areaid:
                # 间谍
                if self.account.user.spy_areaid > 0:
                    await self.attack_spy(self.account.user.spy_areaid, area_info)

                # 悬赏
                if city_event_config["enable"]:
                    event_info = await world.getNewCityEventInfo(self.account)
                    if event_info:
                        # 悬赏目标
                        if area_info["悬赏目标"] != 0:
                            await self.attack_city_event_player(area_info["悬赏目标城池"], area_info["悬赏目标城区"], area_info["悬赏目标"])

                # 搜索敌人
                if attack_config["enable"] and attack_config["main_city"][self.account.user.nation] != self.account.user.areaid:
                    can_attack_area_list = await self.attack_player(self.account.user.areaid, area_info)
                    for a_area in can_attack_area_list:
                        # 屠城
                        attack_num = 0
                        total_num = len(a_area["英雄帖玩家列表"]) + len(a_area["玩家列表"]) + len(a_area["NPC列表"]) + len(a_area["已被抓的玩家列表"]) + len(a_area["已被抓的NPC列表"])
                        attack_arrest = False
                        if tu_city_config["enable"] and a_area["屠城"] and self.account.user.tucd == 0 and self.account.user.remaintutimes > 0:
                            if total_num <= tu_city_config["people_num"]:
                                await world.tuCity(self.account, areaId=a_area["城池"])
                                attack_arrest = True
                        attack_list = []
                        attack_list.extend(a_area["英雄帖玩家列表"])
                        attack_list.extend(a_area["玩家列表"])
                        attack_list.extend(a_area["NPC列表"])
                        if attack_arrest:
                            attack_list.extend(a_area["已被抓的玩家列表"])
                            attack_list.extend(a_area["已被抓的NPC列表"])
                        for city in attack_list:
                            lost_times = 0
                            while True:
                                result, error, arrest_state, attack_back = await world.attackOtherAreaCity(self.account, areaId=city["areaid"], scopeId=city["scopeid"], cityId=city["cityid"])
                                if result is False:
                                    if error == "没有足够的攻击令":
                                        if attack_arrest:
                                            await world.getTranferInfo(self.account)
                                            treasure_num = await world.getNewAreaTreasureInfo(self.account)
                                            while treasure_num > treasure_config["arrest_reserve"]:
                                                await world.draw5NewAreaTreasure(self.account)
                                                treasure_num -= 5
                                        if self.account.user.atttoken <= 0:
                                            return self.immediate
                                    elif error == "军令还没有冷却，请等待":
                                        return self.immediate
                                    elif error == "你已被抓，请先逃跑":
                                        return self.immediate
                                    elif error == "您当前正在组队征战中，不可以进行其他操作":
                                        return self.ten_minute
                                    elif error == "该位置玩家发生了变动":
                                        attack_num += 1
                                        break
                                    elif error == "打不过敌人":
                                        lost_times += 1
                                        if lost_times >= attack_config["lost_times"]:
                                            break
                                    else:
                                        break
                                else:
                                    if self.account.user.spy_areaid > 0:
                                        await self.attack_spy(self.account.user.spy_areaid, area_info)
                                    if attack_back:
                                        attack_num += 1
                                        break
                                    elif arrest_state and not attack_arrest:
                                        break
                        if attack_arrest and attack_num == total_num:
                            self.logger.info("完成屠城")
                            next_area = await self.get_next_move_area(a_area["城池"], area_info)
                            if next_area is not None:
                                await world.cdMoveRecoverConfirm(self.account)
                                await world.transferInNewArea(self.account, areaId=next_area["areaid"], area=next_area)
                                return self.immediate

        # 悬赏
        if city_event_config["enable"]:
            event_info = await world.getNewCityEventInfo(self.account)
            # 领取悬赏任务
            if not event_info["悬赏已完成"] and event_info["悬赏剩余时间"] <= 0 and event_info["悬赏剩余次数"] > city_event_config["reserve"] and len(event_info["悬赏任务列表"]) > 0:
                for task in event_info["悬赏任务列表"]:
                    if task["星级"] <= city_event_config["star"]:
                        await world.acceptNewCityEvent(self.account, pos=task["位置"], task=task)
                        break

        # 决斗
        area_list = self.get_neighbors_area(self.account.user.areaid, area_info)
        for a_area in area_list:
            if a_area["areaname"] in attack_config["exculde"] and a_area["areaid"] != attack_config["main_city"][self.account.user.nation]:
                await self.duel(a_area, area_info, attack_config["diff_level"], attack_config["duel_city_hp_limit"])
                break

        # 移动cd
        if area_info["移动cd"] > 0:
            if area_info["免费移动次数"] > attack_config["reserve_transfer_cd_clear_num"]:
                await world.cdMoveRecoverConfirm(self.account)
            else:
                return area_info["移动cd"] // 1000

        # # 封地生产
        # if fengdi_config["enable"]:
        #     fengdi = self.account.user.fengdi
        #     if fengdi.nextcd == 0 and fengdi.remainnum > 0:
        #         if len(area_info["封地城池"]) > 0:
        #             for area_id, a_area in area_info["封地城池"].items():
        #                 if a_area["fengdicd"] >= fengdi_config["cd"]:
        #                     next_area = await self.get_next_move_area(area_id, area_info)
        #                     if next_area is not None:
        #                         await world.transferInNewArea(self.account, areaId=area_id, area=next_area)
        #                         return self.immediate
        #     elif fengdi.nextcd > 0:
        #         return self.one_minute

        # 集结
        if nation_task_info["集结城池"]:
            self.logger.info("发现集结城池[%s]", nation_task_info["集结城池"])
            next_area = await self.get_next_move_area(nation_task_info["集结城池"], area_info)
            if next_area is not None:
                await world.transferInNewArea(self.account, areaId=next_area["areaid"], area=next_area)
                return self.immediate

        # 间谍
        if self.account.user.spy_areaid > 0:
            next_area = await self.get_next_move_area(self.account.user.spy_areaid, area_info)
            if next_area is not None:
                await world.transferInNewArea(self.account, areaId=next_area["areaid"], area=next_area)
                return self.immediate

        # 随机屠城
        if tu_city_config["enable"] and self.account.user.tucd == 0 and self.account.user.remaintutimes > 0 and event_info["悬赏剩余次数"] == 0:
            for a_area in area_info["所有城池"].values():
                if a_area["nation"] != self.account.user.nation and a_area["areaname"] not in attack_config["exculde"]:
                    await world.tuCity(self.account, areaId=a_area["areaid"])
                    return self.immediate

        # 敌方都城附近
        near_main_city_area_id_list = attack_config["near_main_city"][self.account.user.nation]
        for area_id in near_main_city_area_id_list:
            if area_id == self.account.user.areaid:
                if self.account.user.atttoken == 0 and not self.can_duel(attack_config["duel_city_hp_limit"], area_info):
                    return self.next_half_hour
                return self.immediate
        for area_id in near_main_city_area_id_list:
            next_area = await self.get_next_move_area(area_id, area_info)
            if next_area is not None:
                await world.transferInNewArea(self.account, areaId=next_area["areaid"], area=next_area)
                return self.immediate

        # 取一个方向前进
        self.account.user.astar.ignore_barrier(True)
        for area_id in near_main_city_area_id_list:
            next_area = await self.get_next_move_area(area_id, area_info)
            if next_area is not None:
                if await world.transferInNewArea(self.account, areaId=next_area["areaid"], area=next_area):
                    return self.immediate
                else:
                    self.account.user.transfer_fail_num += 1
                if self.account.user.transfer_fail_num >= attack_config["transfer_fail_num"]:
                    self.account.user.transfer_fail_num = 0
                    return self.next_hour
                return self.one_minute

        return self.one_minute

    async def do_duel(self):
        while True:
            pk_info = await world.getPkInfo(self.account, type=0)
            if pk_info and pk_info["阶段"] == 1:
                gong = pk_info["攻"]
                fang = pk_info["防"]
                target = pk_info["目标"]
                self.logger.info("%s(%d/%d) VS %s(%d/%d)", gong["玩家"], gong["城防"], gong["最大城防"], fang["玩家"], fang["城防"], fang["最大城防"])
                await world.attackOtherAreaCity(self.account, areaId=target["城池"], scopeId=target["区域"], cityId=target["城市"])
            else:
                break

    def can_duel(self, duel_city_hp_limit, area_info):
        return self.account.user.cityhp > duel_city_hp_limit and area_info["诱敌锦囊"] > 0 and area_info["决斗战旗"] > 0

    async def duel(self, a_area, area_info, diff_level, duel_city_hp_limit):
        scope_id = 1
        while self.can_duel(duel_city_hp_limit, area_info):
            city_list = await area.getAllCity(self.account, areaId=a_area["areaid"], scopeId=scope_id)
            if city_list is None:
                break
            for city in city_list:
                if not self.can_duel(duel_city_hp_limit, area_info):
                    break
                level = city["citylevel"]
                if 0 <= self.account.user.playerlevel - level <= diff_level:
                    result, info, error_code = await world.useWorldDaoju(self.account, areaId=city["areaid"], scopeId=city["scopeid"], cityId=city["cityid"], type=2, desc="使用诱敌锦囊", city=city)
                    if result:
                        area_info["诱敌锦囊"] -= 1
                        duel_city_list = await area.getAllCity(self.account, areaId=info["城池"], scopeId=info["区域"])
                        if duel_city_list is None:
                            return
                        for duel_city in duel_city_list:
                            if duel_city["playerid"] == info["玩家"]:
                                result, info, error_code = await world.useWorldDaoju(self.account, areaId=duel_city["areaid"], scopeId=duel_city["scopeid"], cityId=duel_city["cityid"], type=1, desc="使用决斗战旗", city=duel_city)
                                if result:
                                    area_info["决斗战旗"] -= 1
                                    await self.do_duel()
                                    break
                                else:
                                    return
                    elif "当前城池正在补充城防" in error_code or "该玩家今日诱敌次数已满" in error_code:
                        continue
                    else:
                        return
            scope_id += 1

    async def attack_spy(self, area_id, area_info):
        area_list = self.get_neighbors_area(area_id, area_info, True)
        for a_area in area_list:
            if area_id == a_area["areaid"]:
                self.account.user.spy_areaid = 0
                for i in range(1, 100):
                    city_list = await area.getAllCity(self.account, areaId=area_id, scopeId=i)
                    if city_list is None:
                        break
                    for city in city_list:
                        if city["myspy"] == 0:
                            continue
                        await world.attackOtherAreaCity(self.account, areaId=area_id, scopeId=i, cityId=city["cityid"])
                break

    def get_neighbors_area(self, area_id, area_info, include_me=False, exclude=None):
        neighbors_area_list = []
        a_area = area_info["城池ID"][area_id]
        if include_me:
            neighbors_area_list.append(a_area)
        # coordinate = list(map(int, a_area["coordinate"].split(",")))
        coordinate = a_area["coordinate"]
        y, x = coordinate[0] - 1, coordinate[1] - 1
        astar = self.account.user.astar
        for ny, nx in [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]:
            if 0 <= nx < astar.m_nWidth and 0 <= ny < astar.m_nHeight and (n_area := area_info["所有城池"].get((ny, nx))) is not None:
                if exclude is None or n_area["areaname"] not in exclude:
                    neighbors_area_list.append(n_area)
        return neighbors_area_list
    
    async def attack_city_event_player(self, area_id, scope_id, player_id):
        city_list = await area.getAllCity(self.account, areaId=area_id, scopeId=scope_id)
        if city_list is None:
            return
        for city in city_list:
            if city["playerid"] == player_id:
                if city["protectcd"] == 0:
                    await world.attackOtherAreaCity(self.account, areaId=area_id, scopeId=scope_id, cityId=city["cityid"])
                break

    async def attack_player(self, area_id, area_info):
        area_list = self.get_neighbors_area(area_id, area_info, True, config["world"]["attack"]["exculde"])
        can_attack_area_list = []
        for a_area in area_list:
            if a_area["nation"] == self.account.user.nation:
                can_tu_city = False
            else:
                can_tu_city = True
            can_attack_player = []
            can_attack_npc = []
            arrest_player = []
            arrest_npc = []
            pvp_attack_player = []
            for i in range(1, 100):
                city_list = await area.getAllCity(self.account, areaId=a_area["areaid"], scopeId=i)
                if city_list is None:
                    break
                for city in city_list:
                    if city["nation"] == self.account.user.nation:
                        continue
                    if city["protectcd"] != 0:
                        can_tu_city = False
                        continue
                    if city["citytype"] == 1:
                        if city["citylevel"] > self.account.user.playerlevel:
                            can_tu_city = False
                        elif city["inpk"] != 0:
                            can_tu_city = False
                        elif city["arreststate"] == 0:
                            if city.get("heronote", 0) == 2:
                                pvp_attack_player.append(city)
                            else:
                                can_attack_player.append(city)
                        else:
                            arrest_player.append(city)
                    elif city["arreststate"] == 0:
                        can_attack_npc.append(city)
                    else:
                        arrest_npc.append(city)
            can_attack_area_list.append({"城池": a_area["areaid"], "屠城": can_tu_city, "英雄帖玩家列表": pvp_attack_player, "玩家列表": can_attack_player, "NPC列表": can_attack_npc, "已被抓的玩家列表": arrest_player, "已被抓的NPC列表": arrest_npc})
        return can_attack_area_list

    async def get_next_move_area(self, area_id, area_info):
        current_area = area_info["城池ID"][self.account.user.areaid]
        goal_area = None

        if isinstance(area_id, str):
            goal_area = area_info["城池名"][area_id]
        elif isinstance(area_id, int):
            goal_area = area_info["城池ID"][area_id]
        elif isinstance(area_id, tuple):
            goal_area = area_info["所有城池"][area_id]

        if goal_area is None or current_area is None:
            self.logger.info("area type is %s, not str or int or tuple", type(area_id))
            return None

        if current_area["areaid"] == goal_area["areaid"]:
            self.logger.info("已在城池[%s]", current_area["areaname"])
            return None

        # coordinate = list(map(int, current_area["coordinate"].split(",")))
        coordinate = current_area["coordinate"]
        current_y, current_x = coordinate[0] - 1, coordinate[1] - 1
        # coordinate = list(map(int, goal_area["coordinate"].split(",")))
        coordinate = goal_area["coordinate"]
        goal_y, goal_x = coordinate[0] - 1, coordinate[1] - 1
        paths = self.account.user.astar.astar((current_y, current_x), (goal_y, goal_x))
        if paths is None:
            self.logger.warning("从城池[%s]无法到达城池[%s]", current_area["areaname"], goal_area["areaname"])
            return None

        path_list = list(paths)
        path_list.pop(0)
        self.logger.info("从城池[%s]到达城池[%s], 需要经过城池%s", current_area["areaname"], goal_area["areaname"], " ".join(area_info["所有城池"][path]["areaname"] for path in path_list))
        return area_info["所有城池"][path_list[0]]
