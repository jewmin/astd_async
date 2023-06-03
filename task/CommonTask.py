# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class CommonTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "通用"

    async def Init(self):
        await self._Exec()

    async def _Exec(self):
        await server.getPlayerInfoByUserId(self.account)
        await server.getExtraInfo(self.account)
        await server.getAntiAddictionInfo(self.account)
        await mainCity.mainCity(self.account)
        await equip.getUpgradeInfo(self.account, show=True)

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
            await officer.officer(self.account)

        # 将军塔
        await mainCity.getGeneralTowerInfo(self.account)
        if config["mainCity"]["auto_build_general_tower"]:
            while self.account.user.generaltower.buildingstone > 100:
                await mainCity.useBuildingStone(self.account, buildMode=1)

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

        # 征收活动
        await gift.getEventGiftInfo(self.account)

        # 军资回馈
        info = await gift.getRepayEventGiftInfo(self.account)
        if info is not None:
            for index, status in enumerate(info["领取状态"]):
                if status == 1:
                    await gift.receiveRepayEventReward(self.account, id=info["奖励"][index])

        self.logger.warning("活动列表: %s", self.account.user.HaveActivities())
        return self.next_half_hour
