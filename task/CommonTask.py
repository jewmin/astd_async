from task.BaseTask import BaseTask
import protocol.server as server


class CommonTask(BaseTask):
    """通用任务"""
    def __init__(self, account):
        super().__init__(account)
        self.name = "通用"

    async def _Exec(self):
        await server.getExtraInfo(self.account)
        await server.getPlayerExtraInfo2(self.account)
        return self.next_half_hour
        # city_mgr.get_main_city()
        # equip_mgr.get_upgrade_info()

        # # 登录奖励
        # if config["mainCity"]["auto_get_login_reward"]:
        #     # 今日手气
        #     if self.m_objUser.m_bHasPerDayReward:
        #         city_mgr.get_per_day_reward()
        #     # 礼包
        #     misc_mgr.get_new_gift_list()
        #     # 登录签到送礼
        #     city_mgr.get_login_reward_info()
        #     # 恭贺
        #     city_mgr.get_champion_info()
        #     # 俸禄
        #     misc_mgr.officer()

        # # 将军塔
        # city_mgr.get_general_tower_info(config["mainCity"]["auto_build_general_tower"])

        # # 免费征兵
        # if config["mainCity"]["auto_right_army"]:
        #     if self.m_objUser.m_nRightNum > 0 and self.m_objUser.m_nRightCd == 0:
        #         city_mgr.right_army()

        # # 日常任务
        # if config["task"]["auto_task"]:
        #     misc_mgr.get_new_per_day_task()

        # # 采集宝石
        # if config["outCity"]["auto_end_bao_shi_pick"]:
        #     city_mgr.get_pick_space(config["outCity"]["end_pick_proportion"])

        # # 自动领取军令
        # if config["mainCity"]["auto_apply_token"]:
        #     misc_mgr.secretary()

        # # 自动技术研究
        # if config["outCity"]["auto_tech_research"]:
        #     city_mgr.jail(self.get_available_gold(), config["outCity"]["jail_baoshi"])

        # # 自动委派
        # if config["mainCity"]["auto_trade"]:
        #     misc_mgr.get_player_merchant()