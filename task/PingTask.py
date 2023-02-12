from task.BaseTask import BaseTask
import protocol.server as server


class PingTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "会话保持"

    async def _Exec(self):
        await server.getServerTime(self.account)
        await server.getPlayerExtraInfo2(self.account)
        return self.two_minute
