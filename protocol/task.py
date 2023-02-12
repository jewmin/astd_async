import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("日常任务")
async def getNewPerdayTask(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        dayboxstate: str = result.result["dayboxstate"]
        for k, v in enumerate(dayboxstate.split(","), 1):
            if v == "0":
                await openDayBox(account, rewardId=k)

        if result.result["redpacketinfo"]["redpacket"] == "0":
            await openWeekRedPacket(account)

        account.user.task.HandleXml("task", result.result["task"])
        for task in account.user.task.values():
            if task.taskstate == 3:
                await getNewPerdayTaskReward(account, rewardId=task.taskid)


@ProtocolMgr.Protocol("日常任务 - 开启宝箱", ("rewardId",))
async def openDayBox(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("日常任务, 开启宝箱, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("日常任务 - 开启活跃红包")
async def openWeekRedPacket(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("日常任务, 开启活跃红包, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("日常任务 - 领奖", ("rewardId",))
async def getNewPerdayTaskReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.logger.info("日常任务, 领奖, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405
