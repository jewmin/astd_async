# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class BombNianEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<抓年兽>"
        self.type = "boatevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await bombNianEvent.getBombNianInfo(self.account)
        if info is None:
            return self.next_half_hour

        if "排名奖励状态" in info and info["排名奖励状态"] == 0:
            await bombNianEvent.getRankReward(self.account)

        if info["领奖状态"] == 1:
            info["奖励"] = sorted(info["奖励"], key=lambda reward: self.GetConfig("reward_index", {}).get(reward["rewardinfo"]["reward"]["type"], 99))
            for reward_info in info["奖励"]:
                if reward_info["state"] == 1:
                    await bombNianEvent.openGift(self.account, giftId=reward_info["id"])
            return self.immediate
        else:
            self.account.logger.info("年兽血量: %d/%d", info["年兽血量"], info["年兽最大血量"])
            for idx, hp in enumerate(self.GetConfig("hp")):
                if info["年兽血量"] >= hp:
                    info["鞭炮"] = sorted(info["鞭炮"], key=lambda obj: self.GetConfig("bomb")[idx][obj["类型"]])
                    for bomb in info["鞭炮"]:
                        if bomb["花费金币"] <= self.GetConfig("gold")[bomb["类型"]] and bomb["花费金币"] <= self.GetAvailableGold():
                            await bombNianEvent.bombNian(self.account, bombType=bomb["类型"], cost=bomb["花费金币"])
                            return self.immediate
            await bombNianEvent.huntNian(self.account)

        return self.next_half_hour
