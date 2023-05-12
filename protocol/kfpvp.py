import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("英雄帖")
async def getSignupList(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "报名状态": result.GetValue("message.signupstate"),
            "宝箱": result.GetValue("message.playerboxinfo.boxnum"),
            "冷却时间": result.GetValue("message.cd"),
            "免费鼓舞次数": result.GetValue("message.freeinspire"),
            "徽章": result.GetValue("message.medalstate"),
        }
        return info


@ProtocolMgr.Protocol("英雄帖报名")
async def signUp(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("英雄帖报名")


@ProtocolMgr.Protocol("开启英雄帖宝箱", ("gold",))
async def openBoxById(account: 'Account', result: 'ServerResult', gold):
    if result.success:
        reward = Reward()  # noqa: F405
        reward.type = 42
        reward.num = result.GetValue("message.tickets")
        reward.itemname = "点券"
        reward.lv = 1
        reward_info = RewardInfo(result.result["message"]["rewardinfo"])  # noqa: F405
        reward_info.reward.append(reward)
        account.logger.info("开启英雄帖宝箱, 获得%s", reward_info)


@ProtocolMgr.Protocol("英雄帖比赛详情")
async def getMatchDetail(account: 'Account', result: 'ServerResult'):
    if result.success:
        detail = {
            "积分奖励": result.GetValue("message.scoreticketsreward", 0) == 1,
            "免费鼓舞": result.GetValue("message.freeinspire", 0),
            "可以鼓舞": result.GetValue("message.caninspire", 0) == 1,
            "冷却时间": result.GetValue("message.cd", 0),
            "攻方": result.GetValue("message.attacker"),
            "守方": result.GetValue("message.defender"),
        }
        return detail


@ProtocolMgr.Protocol("跨服PVP鼓舞", ("count",))
async def inspire(account: 'Account', result: 'ServerResult', count):
    if result.success:
        account.logger.info("跨服PVP鼓舞")


@ProtocolMgr.Protocol("英雄帖结算详情")
async def getTributeDetail(account: 'Account', result: 'ServerResult'):
    if result.success:
        detail = {
            "初始排名": result.GetValue("message.expectrank"),
            "最终排名": result.GetValue("message.finalrank"),
            "最终排名奖励": result.GetValue("message.cangetfinalreward", 0) == 1,
            "最终排名前三奖励": result.GetValue("message.cangettopreward", 0) == 1,
            "徽章": result.GetValue("message.medalstate"),
        }
        return detail


@ProtocolMgr.Protocol("英雄帖最终排名奖励", ("rewardId",))
async def recvRewardById(account: 'Account', result: 'ServerResult', rewardId):
    if result.success:
        account.logger.info("领取英雄帖最终排名奖励, 获得宝箱+%d", result.GetValue("message.rewardbox"))


@ProtocolMgr.Protocol("领取英雄帖勋章奖励")
async def recvWdMedal(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取英雄帖勋章奖励, 获得%s", result.GetValue("message.wdmedalname"))
