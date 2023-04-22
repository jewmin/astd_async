# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *
from model.child import *  # noqa: F403


class SpringFestivalWishEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<许愿>"
        self.type = "springfestivalwishevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await springFestivalWish.getSpringFestivalWishInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["许愿状态"] == 1:  # 辞旧岁
            if info["下一福利"] is not None:
                reward_info = RewardInfo(info["下一福利"]["rewardinfo"])  # noqa: F405
                await springFestivalWish.hangInTheTree(self.account, reward_info=reward_info)
                return self.immediate
            elif info["可领奖状态"] == 0:
                await springFestivalWish.openCijiuReward(self.account)
                return self.immediate

        elif info["许愿状态"] == 2:  # 迎新年
            if info["可领奖状态"] == 0:
                await springFestivalWish.openYinxingReward(self.account)
                return self.immediate

        elif info["许愿状态"] == 3:  # 领奖
            if info["愿望"] is not None:
                for idx, wish in enumerate(info["愿望"], 1):
                    if wish == 0:
                        await springFestivalWish.receiveWishReward(self.account, id=idx)
                return self.immediate

        return self.next_half_hour
