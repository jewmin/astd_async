# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class DayTreasureGameTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "王朝寻宝"

    async def _Exec(self):
        if config["dayTreasureGame"]["enable"]:
            dict_info = await dayTreasureGame.startNewTGame(self.account)
            if dict_info is not None:
                if "事件" in dict_info:
                    await self.handle_event(dict_info)
                    return self.immediate

                if dict_info["换地图"]:
                    await dayTreasureGame.transfer(self.account)
                    return self.immediate

                if dict_info["探宝完毕"]:
                    await dayTreasureGame.awayNewTGame(self.account)
                    return self.immediate

                if self.account.user.curactive / self.account.user.maxactive <= config["dayTreasureGame"]["active_proportion"]:
                    if dict_info["当前骰子"] > 0:
                        await dayTreasureGame.useNewTDice(self.account)
                        return self.immediate

        return self.next_half_hour

    async def handle_event(self, dict_info):
        if dict_info["事件"] == 1:
            await dayTreasureGame.handlerEvent(self.account, open=1, msg=f"执行{dict_info['事件名称']}")

        elif dict_info["事件"] == 2:
            if dict_info["免费摇摇钱树"] > 0:
                await dayTreasureGame.handlerEvent(self.account, open=1, msg=f"执行{dict_info['事件名称']}")
            else:
                await dayTreasureGame.handlerEvent(self.account, open=0, msg=f"取消{dict_info['事件名称']}")

        elif dict_info["事件"] == 3:
            await dayTreasureGame.handlerEvent(self.account, open=0, msg=f"取消{dict_info['事件名称']}")
