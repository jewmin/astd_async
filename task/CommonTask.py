from logic.Config import config
from task.BaseTask import BaseTask
import protocol.server as server
import protocol.mainCity as mainCity
import protocol.task as task
import protocol.newGift as newGift
import protocol.outCity as outCity
import protocol.secretary as secretary
import protocol.market as market
import protocol.jail as jail
import protocol.officer as officer


class CommonTask(BaseTask):
    """通用任务"""
    def __init__(self, account):
        super().__init__(account)
        self.name = "通用"

    async def _Exec(self):
        await server.getExtraInfo(self.account)
        await server.getPlayerExtraInfo2(self.account)
        await mainCity.mainCity(self.account)
        # equip_mgr.get_upgrade_info()

        # 登录奖励
        if config["mainCity"]["auto_get_login_reward"]:
            # 今日手气
            if self.account.user.perdayreward:
                await mainCity.getPerDayReward(self.account)
            # 礼包
            await newGift.doGetNewGiftList(self.account)
            # 登录签到送礼
            await mainCity.getLoginRewardInfo(self.account)
            # 恭贺
            await mainCity.getChampionInfo(self.account)
            # 俸禄
            officer.officer(self.account)

        # 将军塔
        tower = await mainCity.getGeneralTowerInfo(self.account)
        if config["mainCity"]["auto_build_general_tower"]:
            while tower.buildingstone > 0:
                tower = await mainCity.useBuildingStone(self.account, buildMode=1)

        # 免费征兵
        if config["mainCity"]["auto_right_army"]:
            if self.account.user.rightnum > 0 and self.account.user.rightcd == 0:
                await mainCity.rightArmy(self.account)

        # 日常任务
        if config["task"]["auto_task"]:
            await task.getNewPerdayTask(self.account)

        # 采集宝石
        if config["outCity"]["auto_end_bao_shi_pick"]:
            await outCity.doGetPickSpace(self.account, config["outCity"]["end_pick_proportion"])

        # 自动领取军令
        if config["mainCity"]["auto_apply_token"]:
            await secretary.secretary(self.account)

        # 自动技术研究
        if config["outCity"]["auto_tech_research"]:
            await jail.doJail(self.account, config["outCity"]["jail_baoshi"])

        # 自动委派
        if config["mainCity"]["auto_trade"]:
            await market.getPlayerMerchant(self.account)

        return self.next_half_hour
