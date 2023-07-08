# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class SnowTrading(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<雪地通商>"
        self.type = "snowtradingevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await snowTrading.getSnowTradingInfo(self.account)
        if info is None:
            return self.next_half_hour

        for case in info["奖励"]:
            if case["state"] == 1:
                await snowTrading.getCaseNumReward(self.account, cases=case["id"])

        if info["免费通商次数"] > 0:
            reinforce_config = self.GetConfig("reinforce")
            if reinforce_config["enable"]:
                if not info["已加固雪橇"] and info["宝箱类型"] >= reinforce_config["type"] and info["加固雪橇花费金币"] <= reinforce_config["cost"] and self.IsAvailableAndSubGold(info["加固雪橇花费金币"]):
                    await snowTrading.reinforceSled(self.account, cost=info["加固雪橇花费金币"])
                    return self.immediate
            await snowTrading.transport(self.account, choose=self.GetConfig("choose"), cast_type=info["宝箱类型"])
            return self.immediate
        elif info["购买次数花费金币"] <= self.GetConfig("buyroundcost") and self.IsAvailableAndSubGold(info["购买次数花费金币"]):
            await snowTrading.buyRound(self.account, cost=info["购买次数花费金币"])
            return self.immediate

        return self.next_half_hour
