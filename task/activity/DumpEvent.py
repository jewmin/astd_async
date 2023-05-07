# flake8: noqa
from task.activity.ActivityTask import ActivityTask
from protocol import *


class DumpEvent(ActivityTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动<宝石倾销>"
        self.type = "dumpevent"

    async def _Exec(self):
        if not self.Enable():
            return self.next_half_hour

        info = await dumpEvent.getDetail(self.account)
        if info is None:
            return self.next_half_hour

        while info["商品"]["numleft"] > 0:
            info["商品"]["numleft"] -= 1
            await dumpEvent.buy(self.account, id=info["商品"]["id"], good=info["商品"])

        while info["锦囊"] > 0:
            info["锦囊"] -= 20
            await dumpEvent.openBags(self.account, num=20)

        return self.next_half_hour
