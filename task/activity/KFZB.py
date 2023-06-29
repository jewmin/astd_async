# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class KFZB(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<群雄争霸>"
        self.type = "worldpk"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await kfzb.getMatchDetail(self.account)
        if info is None:
            return self.ten_minute

        if info["可以鼓舞"] and info["鼓舞花费金币"] <= 0:
            if info["攻方"]["playerlevel"] >= info["守方"]["playerlevel"]:
                await kfzb.support(self.account, competitorId=info["攻方"]["competitorid"], playername=info["攻方"]["playername"], cost=info["鼓舞花费金币"])
            else:
                await kfzb.support(self.account, competitorId=info["守方"]["competitorid"], playername=info["守方"]["playername"], cost=info["鼓舞花费金币"])
            return self.immediate

        return self.one_minute
