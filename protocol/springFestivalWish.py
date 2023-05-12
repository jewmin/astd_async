import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("许愿界面")
async def getSpringFestivalWishInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "许愿状态": result.GetValue("nowevent"),
            "下一福利": result.GetValue("nextfu"),
            "可领奖状态": result.GetValue("cangetreward", 0),
            "愿望": result.GetValueList("wishstate"),
        }
        return info


@ProtocolMgr.Protocol("挂许愿树")
async def hangInTheTree(account: 'Account', result: 'ServerResult', reward_info):
    if result.success:
        account.logger.info("挂许愿树, 获得%s", reward_info)


@ProtocolMgr.Protocol("辞旧岁")
async def openCijiuReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("辞旧岁, 获得%s", reward_info)


@ProtocolMgr.Protocol("迎新年")
async def openYinxingReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("迎新年, 获得%s", reward_info)


@ProtocolMgr.Protocol("愿望", ("id",))
async def receiveWishReward(account: 'Account', result: 'ServerResult', id):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("愿望, 获得%s", reward_info)
