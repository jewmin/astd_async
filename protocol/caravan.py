import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("西域通商")
async def getWesternTradeInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "商人们": result.GetValue("tradeinfo"),
            "进入下一站": result.GetValue("needclicknext", 0) == 1,
        }
        if (event_type := result.GetValue("eventtype", 0)) != 0:
            handle_western_trade_event(account, result, event_type, dict_info)
        return dict_info


def handle_western_trade_event(account: 'Account', result: 'ServerResult', event_type: int, dict_info: dict):
    dict_info["事件"] = event_type
    if event_type == 1:
        dict_info["双倍奖励消耗金币"] = result.GetValue("doublecost")
        dict_info["可领取状态"] = result.GetValue("firststatus") != 2 and result.GetValue("secondstatus") != 2
        dict_info["位置"] = 0
        num = 0
        msg = "西域国王宝箱[ "
        for index, v in enumerate(result.GetValue("box")):
            reward_info = RewardInfo(v["rewardinfo"])  # noqa: F405
            msg += f"{reward_info} "
            reward = reward_info.get_reward(0)
            if reward is not None and reward.num > num:
                dict_info["位置"] = index
                num = reward.num
        msg += "]"

    elif event_type == 2:
        dict_info["可领取状态"] = (result.GetValue("firststatus"), result.GetValue("secondstatus"))
        dict_info["消耗金币"] = []
        msg = "神秘商人宝箱[ "
        for index, v in enumerate(result.GetValue("box")):
            dict_info["消耗金币"].append(v["cost"])
            msg += f"宝箱[花费{v['cost']}金币] "
        msg += "]"

    elif event_type == 3:
        dict_info["双倍奖励消耗金币"] = result.GetValue("doublecost")
        msg = f"西域通商宝箱[{', '.join(str(RewardInfo(v['rewardinfo'])) for v in result.GetValue('box'))}]"  # noqa: F405
    account.logger.info(msg)


@ProtocolMgr.Protocol("西域国王", ("isdouble", "pos"))
async def getKingReward(account: 'Account', result: 'ServerResult', isdouble, pos, cost):
    if result and result.success:
        if isdouble == -1:
            account.logger.info("取消领取西域国王奖励")
        elif isdouble > 0:
            account.logger.info("花费%d金币, 领取双倍西域国王奖励, 获得%s", cost, RewardInfo(result.result["rewardinfo"]))  # noqa: F405
        else:
            account.logger.info("领取西域国王奖励, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("神秘商人", ("isBuy",))
async def getTraderReward(account: 'Account', result: 'ServerResult', isBuy, cost):
    if result and result.success:
        if isBuy == -1:
            account.logger.info("取消购买神秘商人宝箱")
        else:
            account.logger.info("花费%d金币, 购买神秘商人宝箱", cost)


@ProtocolMgr.Protocol("下一站")
async def nextPlace(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("进入下一站")


@ProtocolMgr.Protocol("通商", ("tradeId",))
async def westernTrade(account: 'Account', result: 'ServerResult', tradeId, trader, cost):
    if result and result.success:
        account.logger.info("花费%s, 通商[%s]", ", ".join(f"{k}{v}" for k, v in cost.items()), trader["name"])
        dict_info = {}
        if (event_type := result.GetValue("eventtype", 0)) != 0:
            handle_western_trade_event(account, result, event_type, dict_info)
        return dict_info


@ProtocolMgr.Protocol("通商奖励", ("isdouble",))
async def getWesternTradeReward(account: 'Account', result: 'ServerResult', isdouble, cost):
    if result and result.success:
        if isdouble > 0:
            account.logger.info("花费%d金币, 领取双倍通商奖励, 获得%s", cost, RewardInfo(result.result["rewardinfo"]))  # noqa: F405
        else:
            account.logger.info("领取通商奖励, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405
