# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class YuanDanQiFu(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<酒神觉醒>"
        self.type = "yuandanqifu"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await yuandanqifu.getQifuEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        self.account.logger.info("福气: %d/%d", info["福气"], info["最大福气"])

        if info["类型"] in self.GetConfig("type"):
            if info["状态"] == 0:
                if info["祈福花费金币"] <= self.GetConfig("gold") and self.IsAvailableAndSubGold(info["祈福花费金币"]):
                    await yuandanqifu.startQifu(self.account, cost=info["祈福花费金币"])
                    return self.immediate
            elif info["状态"] == 1:
                if info["福气"] >= info["最大福气"]:
                    await yuandanqifu.qifuActive(self.account)
                await yuandanqifu.qifuChoose(self.account, indexId=2)
                return self.immediate
            elif info["状态"] == 2:
                if info["本次祈福倍数"] >= self.GetConfig("all_open_xs") and info["全开花费金币"] <= self.GetConfig("all_open_gold") and self.IsAvailableAndSubGold(info["全开花费金币"]):
                    if info["福气"] >= info["最大福气"]:
                        await yuandanqifu.qifuActive(self.account)
                    await yuandanqifu.qifuChooseAll(self.account, cost=info["全开花费金币"])
                    return self.immediate
                else:
                    await yuandanqifu.nextQifu(self.account)
                    return self.immediate

        return self.next_half_hour
