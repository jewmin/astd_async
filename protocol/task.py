import manager.ProtocolMgr as ProtocolMgr
from model.child.RewardInfo import RewardInfo

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol(ProtocolMgr.GET, "日常任务")
async def getNewPerdayTask(account: 'Account', result: 'ServerResult'):
    if result.success:
        dayboxstate: str = result.result["dayboxstate"]
        for k, v in enumerate(dayboxstate.split(","), 1):
            if v == "0":
                await openDayBox(rewardId=k)

        if result.result["redpacketinfo"]["redpacket"] == "0":
            await openWeekRedPacket()

        account.user.task.HandleXml("task", result.result["task"])
        for task in account.user.task.values():
            if task.taskstate == 3:
                await getNewPerdayTaskReward(rewardId=task.taskid)


@ProtocolMgr.Protocol(ProtocolMgr.POST, "日常任务 - 开启宝箱")
async def openDayBox(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo()
        reward_info.HandleXml(result.result["rewardinfo"])
        account.logger.info("日常任务, 开启宝箱, 获得%s", reward_info)


@ProtocolMgr.Protocol(ProtocolMgr.GET, "日常任务 - 开启活跃红包")
async def openWeekRedPacket(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo()
        reward_info.HandleXml(result.result["rewardinfo"])
        account.logger.info("日常任务, 开启活跃红包, 获得%s", reward_info)


@ProtocolMgr.Protocol(ProtocolMgr.POST, "日常任务 - 领奖")
async def getNewPerdayTaskReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo()
        reward_info.HandleXml(result.result["rewardinfo"])
        account.logger.info("日常任务, 领奖, 获得%s", reward_info)
