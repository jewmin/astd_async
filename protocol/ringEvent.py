import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("新年敲钟")
async def getRingEventInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "奖励": result.GetValueList("ringstate"),
            "对联状态": result.GetValue("reelstatus"),
            "敲钟": [
                {"免费次数": result.GetValue("randomtimes"), "花费金币": result.GetValue("randomcost")},
                {"免费次数": result.GetValue("firsttimes"), "花费金币": result.GetValue("firstcost")},
                {"免费次数": result.GetValue("secondtimes"), "花费金币": result.GetValue("secondcost")},
                {"免费次数": result.GetValue("thirdtimes"), "花费金币": result.GetValue("thirdcost")},
            ],
            "对联": result.GetValue("need", ()),
            "已激活次数": result.GetValue("reelnum", 0),
            "红包": result.GetValue("redpapernum", 0),
        }
        return info


@ProtocolMgr.Protocol("领取进度奖励", ("rewardId", "type"))
async def getProgressReward(account: 'Account', result: 'ServerResult', rewardId, type):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("领取进度奖励, 获得%s", reward_info)


@ProtocolMgr.Protocol("打开对联")
async def openReel(account: 'Account', result: 'ServerResult'):
    reel_tuple = ("随机", "福", "禄", "寿")
    if result.success:
        msg = [f"打开对联: {result.GetValue('words')}"]
        needs = map(int, result.result["need"][:-1].split(","))
        for need in needs:
            msg.append(reel_tuple[need])
        account.logger.info(msg)


@ProtocolMgr.Protocol("敲钟", ("bellId",))
async def ring(account: 'Account', result: 'ServerResult', bellId):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        msg = [f"敲钟, 获得{reward_info}"]
        if "bigreward" in result.result:
            big_reward_info = RewardInfo(result.result["bigreward"]["rewardinfo"])  # noqa: F405
            msg.append(f"{big_reward_info}")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("放弃对联")
async def giveUpReel(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("放弃对联")


@ProtocolMgr.Protocol("领取红包")
async def recvRedPaper(account: 'Account', result: 'ServerResult'):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("领取红包, 获得%s", reward_info)
