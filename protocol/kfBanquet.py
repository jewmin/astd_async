import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("盛宴活动", sub_module=False)
async def kfBanquet(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "加入盛宴免费次数": result.GetValue("canjoinnum", 0),
            "加入盛宴花费金币": result.GetValue("buyjoingold", 0),
            "盛宴房间": result.GetValueList("room"),
            "基础点券": result.GetValue("basedoubletickets", 0),
            "再喝一杯花费金币": result.GetValue("doublegold", 0),
            "所在房间": result.GetValue("inroomrank", 0),
            "状态": result.GetValue("status"),
        }
        return info


@ProtocolMgr.Protocol("加入盛宴", ("room",))
async def joinBanquet(account: 'Account', result: 'ServerResult', room, playername):
    if result.success:
        account.logger.info("参加第%d名[%s]的盛宴", room, playername)


@ProtocolMgr.Protocol("购买邀请券", ("num",))
async def buyBanquetNum(account: 'Account', result: 'ServerResult', num, cost=0):
    if result.success:
        account.logger.info("花费%d金币, 购买%d张邀请券", cost, num)


@ProtocolMgr.Protocol("再喝一杯", ("type",))
async def choosenDouble(account: 'Account', result: 'ServerResult', type, tickets):
    if result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 42
        reward.num = tickets
        reward.itemname = "点券"
        reward.lv = 1
        if type == 1:
            reward.num += result.GetValue("tickets")
            msg = "再喝一杯"
        else:
            msg = "不胜酒力"
        reward_info.reward.append(reward)
        account.logger.info("%s, 获得%s", msg, reward_info)
