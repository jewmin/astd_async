# flake8: noqa
from task.BaseTask import BaseTask
from protocol import *


class PingTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "会话保持"

    async def _Exec(self):
        await server.getServerTime(self.account)
        await server.getPlayerExtraInfo2(self.account)
        self.account.logger.info(self.account.user)
        return self.two_minute
