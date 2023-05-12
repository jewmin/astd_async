import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("雪地通商")
async def getSnowTradingInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "加固雪橇花费金币": result.GetValue("reinforcecost"),
            "购买次数花费金币": result.GetValue("buyroundcost"),
            "免费通商次数": result.GetValue("hastime"),
            "奖励": result.GetValueList("casestate"),
            "已加固雪橇": result.GetValue("reinforce") == 1,
            "宝箱类型": result.GetValue("casttype"),
        }
        return info


@ProtocolMgr.Protocol("领取雪地通商奖励", ("cases",))
async def getCaseNumReward(account: 'Account', result: 'ServerResult', cases):
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("领取雪地通商奖励, 获得%s", reward_info)


@ProtocolMgr.Protocol("购买次数")
async def buyRound(account: 'Account', result: 'ServerResult', cost=0):
    if result.success:
        account.logger.info("花费%d金币, 购买次数", cost)


@ProtocolMgr.Protocol("加固雪橇")
async def reinforceSled(account: 'Account', result: 'ServerResult', cost=0):
    if result.success:
        account.logger.info("花费%d金币, 加固雪橇", cost)


@ProtocolMgr.Protocol("雪地通商", ("choose",))
async def transport(account: 'Account', result: 'ServerResult', choose, cast_type):
    cast_tuple = ("", "木质", "白银", "黄金")
    if result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("雪地通商, 掉落[%s]宝箱+%d, 获得%s", cast_tuple[cast_type], result.GetValue("stonestate.storneloss"), reward_info)
