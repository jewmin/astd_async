import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("大练兵")
async def getInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "状态": result.GetValue("training.trainingstate"),
            "第几轮": result.GetValue("training.round"),
            "部队": list(map(int, result.result["training"]["aramy"])),
            "战旗": list(map(int, result.result["training"]["flags"])),
            "红包": result.GetValue("training.hongbao"),
            "免费重置奖励次数": result.GetValue("training.resettime"),
        }
        return info


@ProtocolMgr.Protocol("开始大练兵")
async def start(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("开始大练兵")


@ProtocolMgr.Protocol("攻击部队", ("army",))
async def attackArmy(account: 'Account', result: 'ServerResult', army, army_name):
    army_tuple = ("", "普通", "精英", "首领")
    if result and result.success:
        account.logger.info("攻击[%s]部队, 获得%d红包", army_tuple[army_name], result.GetValue("addhongbao", 0))


@ProtocolMgr.Protocol("领取战旗奖励", ("hongbao",))
async def recHongbao(account: 'Account', result: 'ServerResult', hongbao):
    if result and result.success:
        account.logger.info("领取战旗奖励, 获得%d红包", result.GetValue("addhongbao", 0))


@ProtocolMgr.Protocol("重置大练兵奖励")
async def resetReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("重置大练兵奖励")


@ProtocolMgr.Protocol("打开大练兵红包")
async def getReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("打开大练兵红包, 获得%s", reward_info)
