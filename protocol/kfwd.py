import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("武斗会")
async def getSignupList(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "报名状态": result.GetValue("message.signupstate", 0),
            "宝箱": result.GetValue("message.playerboxinfo.boxnum", 0),
            "冷却时间": result.GetValue("message.cd", 0),
        }
        return info


@ProtocolMgr.Protocol("武斗会报名")
async def signUp(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("武斗会报名")


@ProtocolMgr.Protocol("开启武斗会宝箱", ("gold",))
async def openBoxById(account: 'Account', result: 'ServerResult', gold):
    if result and result.success:
        reward_info = RewardInfo(result.result["message"]["rewardinfo"])  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 42
        reward.num = result.GetValue("message.tickets")
        reward.itemname = "点券"
        reward.lv = 1
        reward_info.reward.append(reward)
        account.logger.info("开启武斗会宝箱, 获得%s", reward_info)


@ProtocolMgr.Protocol("武斗会比赛详情")
async def getMatchDetail(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        detail = {
            "积分奖励": result.GetValue("message.scoreticketsreward", 0) == 1,
        }
        return detail


@ProtocolMgr.Protocol("武斗会积分奖励")
async def getScoreTicketsReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("武斗会积分奖励, 获得%s宝箱", result.GetValue("message.tickets"))


@ProtocolMgr.Protocol("武斗会结算详情")
async def getTributeDetail(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        detail = {
            "积分奖励": result.GetValue("message.scoreticketsreward", 0) == 1,
            "比赛奖励": result.GetValueList("message.tributeinfo.tributelist.tribute"),
        }
        return detail


@ProtocolMgr.Protocol("武斗会比赛奖励")
async def buyTribute(account: 'Account', result: 'ServerResult', tribute):
    if result and result.success:
        account.logger.info("花费%s金币领取武斗会比赛奖励, 获得%s宝箱", tribute.get("gold", "0"), tribute["tickets"])


@ProtocolMgr.Protocol("武斗会勋章")
async def getWdMedalGift(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "勋章": result.GetValueList("message.medal"),
        }
        return info


@ProtocolMgr.Protocol("领取武斗会勋章奖励", ("medalId",))
async def recvWdMedalGift(account: 'Account', result: 'ServerResult', medalId):
    if result and result.success:
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = result.GetValue("message.baoshi.baoshilevel")
        reward.num = result.GetValue("message.baoshi.baoshinum")
        reward.itemname = "宝石"
        reward_info = RewardInfo()  # noqa: F405
        reward_info.reward.append(reward)
        account.logger.info("领取武斗会勋章奖励, 获得%s", reward_info)
