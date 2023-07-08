# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class RingEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<新年敲钟>"
        self.type = "ringevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await ringEvent.getRingEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        for reward in info["奖励"]:
            if reward["state"] == 1:
                await ringEvent.getProgressReward(self.account, rewardId=reward["id"], type=self.GetConfig("reward"))

        while info["红包"] > 0:
            await ringEvent.recvRedPaper(self.account)
            info["红包"] -= 1

        if info["对联状态"] == 1:
            await ringEvent.openReel(self.account)
            return self.immediate
        elif info["对联状态"] == 2:
            need_reel_num_list = [0, 0, 0, 0]
            reel_list = info["对联"]
            if info["已激活次数"] == 0 and (info["敲钟"][0]["免费次数"] > 0 or info["敲钟"][0]["花费金币"] <= self.GetConfig("cost", 0)):
                for idx in range(1, len(reel_list)):
                    need_reel_num_list[reel_list[idx]] += 1
            else:
                for idx in range(info["已激活次数"], len(reel_list)):
                    need_reel_num_list[reel_list[idx]] += 1
            for bell_id, reel in enumerate(info["敲钟"]):
                num = reel["免费次数"]
                if reel["花费金币"] <= self.GetConfig("cost", 0):
                    num += 2
                if need_reel_num_list[bell_id] > num:
                    await ringEvent.giveUpReel(self.account)
                    return self.immediate
            if info["已激活次数"] == 0:
                if info["敲钟"][0]["免费次数"] > 0:
                    await ringEvent.ring(self.account, bellId=0)
                    return self.immediate
                elif info["敲钟"][0]["花费金币"] <= self.GetConfig("cost", 0) and self.IsAvailableAndSubGold(info["敲钟"][0]["花费金币"]):
                    await ringEvent.ring(self.account, bellId=0)
                    return self.immediate
                else:
                    bell_id = reel_list[0]
                    if info["敲钟"][bell_id]["免费次数"] > 0:
                        await ringEvent.ring(self.account, bellId=bell_id)
                        return self.immediate
                    elif info["敲钟"][bell_id]["花费金币"] <= self.GetConfig("cost", 0) and self.IsAvailableAndSubGold(info["敲钟"][bell_id]["花费金币"]):
                        await ringEvent.ring(self.account, bellId=bell_id)
                        return self.immediate
                    else:
                        await ringEvent.giveUpReel(self.account)
                        return self.immediate
            else:
                bell_id = reel_list[info["已激活次数"]]
                if info["敲钟"][bell_id]["免费次数"] > 0:
                    await ringEvent.ring(self.account, bellId=bell_id)
                    return self.immediate
                elif info["敲钟"][bell_id]["花费金币"] <= self.GetConfig("cost", 0) and self.IsAvailableAndSubGold(info["敲钟"][bell_id]["花费金币"]):
                    await ringEvent.ring(self.account, bellId=bell_id)
                    return self.immediate
                else:
                    await ringEvent.giveUpReel(self.account)
                    return self.immediate
        else:
            for bell_id, reel in enumerate(info["敲钟"]):
                if reel["免费次数"] > 0:
                    await ringEvent.ring(self.account, bellId=bell_id)
                    return self.immediate
                elif reel["花费金币"] <= self.GetConfig("cost", 0) and self.IsAvailableAndSubGold(reel["花费金币"]):
                    await ringEvent.ring(self.account, bellId=bell_id)
                    return self.immediate

        return self.next_half_hour
