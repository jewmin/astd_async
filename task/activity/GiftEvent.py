# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class GiftEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<充值赠礼>"
        self.type = "nationdaygoldboxevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await giftEvent.getGoldBoxEventInfo(self.account)
        if info is None:
            return self.next_half_hour

        if info["在线奖励"] == 1:
            await giftEvent.recvOnlineReward(self.account)
            return self.immediate

        while info["宝箱"] > 0:
            info["宝箱"] -= 1
            await giftEvent.openGoldBoxEvent(self.account)

        return self.next_half_hour
