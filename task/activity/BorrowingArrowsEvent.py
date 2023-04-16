# flake8: noqa
import random
from task.activity.ActivityTask import ActivityTask
from protocol import *


class BorrowingArrowsEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<草船借箭>"
        self.type = "borrowingarrowsevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await borrowingArrowsEvent.getPlayerBorrowingArrowsEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        self.info("草船借箭: 军功(%d/%d), 钥匙(%d), 承重(%d/%d)", info["剩余军功"], info["总军功"], info["钥匙数量"], info["承重"], info["承重上限"])
        info["宝箱"] = sorted(info["宝箱"], key=lambda obj: self.GetConfig("unlock", {}).get(obj["rewardtype"]))

        for idx, s in enumerate(info["钥匙"]):
            if s == 0:
                await borrowingArrowsEvent.getKey(self.account, keyId=idx)

        if info["钥匙数量"] > 0:
            for reward in info["宝箱"]:
                if reward["buynum"] == -1:
                    await borrowingArrowsEvent.unlockReward(self.account, rewardType=reward["rewardtype"])
                    return self.immediate

        for reward in info["宝箱"]:
            if reward["buynum"] != -1:
                cost = reward["cost"]
                if cost <= self.GetConfig("cost_limit", 0) and cost <= info["剩余军功"]:
                    await borrowingArrowsEvent.exchangeReward(self.account, rewardType=reward["rewardtype"])
                    return self.immediate

        if info["状态"] == -2:
            if info["免费发船"] > 0:
                await borrowingArrowsEvent.setSail(self.account, cost=0)
                return self.immediate
            elif info["发船花费金币"] <= self.GetConfig("sail_gold", 0) and info["发船花费金币"] <= self.GetAvailableGold():
                await borrowingArrowsEvent.setSail(self.account, cost=info["发船花费金币"])
                return self.immediate
            else:
                return self.next_half_hour
        elif info["承重上限"] - info["承重"] <= self.GetConfig("arrow_diff", 0):
            await borrowingArrowsEvent.deliverArrows(self.account)
        else:
            await borrowingArrowsEvent.choiceStream(self.account, streamId=random.randint(0, 2))

        return self.immediate
