import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("获取龙舟信息", ("notice",))
async def getBoatEventInfo(account: 'Account', result: 'ServerResult', notice=0):
    if result and result.success:
        info = {
            "组队中": result.GetValue("inteam", 0),
            "阶段": result.GetValue("stage", 0),
            "冲刺花费金币": result.GetValue("dashcost", 100),
            "奖励状态": result.GetValue("signreward.state", 0),
            "剩余次数": result.GetValue("playerboat.remaintimes", 0),
            "龙舟品质": result.GetValue("playerboat.quality", 0),
            "队伍列表": result.GetValueList("team"),
        }
        return info


@ProtocolMgr.Protocol("升级龙舟")
async def upgradeBoat(account: 'Account', result: 'ServerResult', cost):
    if result and result.success:
        account.logger.info("花费%d金币, 升级龙舟", cost)


@ProtocolMgr.Protocol("加入龙舟队伍", ("teamId",))
async def joinBoatEventTeam(account: 'Account', result: 'ServerResult', teamId):
    if result and result.success:
        account.logger.info("加入龙舟队伍[%s]", teamId)


@ProtocolMgr.Protocol("创建龙舟队伍")
async def creatBoatEventTeam(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("创建龙舟队伍")


@ProtocolMgr.Protocol("报名龙舟大赛", ("signUpId",))
async def signUpBoatEvent(account: 'Account', result: 'ServerResult', signUpId=0):
    if result and result.success:
        account.logger.info("报名龙舟大赛")


@ProtocolMgr.Protocol("开始龙舟大赛")
async def startBoatComp(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("开始龙舟大赛")


@ProtocolMgr.Protocol("龙舟冲刺")
async def dashBoatEvent(account: 'Account', result: 'ServerResult', cost):
    if result and result.success:
        if cost > 0:
            account.logger.info("花费%d金币, 龙舟冲刺", cost)
        else:
            account.logger.info("免费, 龙舟冲刺")


@ProtocolMgr.Protocol("领取龙舟大赛奖励")
async def recvBoatEventFinalReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        msg = ["领取龙舟大赛奖励"]
        if "signreward" in result.result:
            reward_info = RewardInfo(result.result["signreward"]["rewardinfo"])  # noqa: F405
            msg.append(f"获得冲刺奖励[{reward_info}]")
        if "rankreward" in result.result:
            reward_info = RewardInfo(result.result["rankreward"]["rewardinfo"])  # noqa: F405
            msg.append(f"获得排名奖励[{reward_info}]")
        if "milesreward" in result.result:
            reward_info = RewardInfo(result.result["milesreward"]["rewardinfo"])  # noqa: F405
            msg.append(f"获得路程奖励[{reward_info}]")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("抓捕活动")
async def getArrestEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "可领取抓捕令": result.GetValue("cangettoken", 0),
            "抓捕令": result.GetValue("arresttokennum", 0),
            "俘虏": result.GetValue("slaves", 0),
            "免费鞭子次数": result.GetValue("freehighshen", 0),
            "鞭子花费金币": result.GetValue("hishengold", 0),
            "粽子数量": result.GetValue("ricedumpling", 0),
            "购买抓捕令花费金币": result.GetValue("arresttokencostgold", 0),
        }
        return info


@ProtocolMgr.Protocol("领取抓捕令")
async def recvArrestToken(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("领取%d抓捕令", result.GetValue("arresttokennum", 0))


@ProtocolMgr.Protocol("审问俘虏", ("highLv",))
async def shenSlaves(account: 'Account', result: 'ServerResult', cost, highLv=0):
    if result and result.success:
        msg = []
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        if cost > 0:
            msg.append(f"花费{cost}金币, 使用鞭子")
        else:
            msg.append("免费, 使用鞭子")
        msg.append(f"审问俘虏, 获得{reward_info}")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("享用端午密粽")
async def eatRiceDumpling(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        reward_info = RewardInfo(result.result["rewardinfo"])  # noqa: F405
        account.logger.info("享用端午密粽, 获得%s", reward_info)


@ProtocolMgr.Protocol("购买抓捕令")
async def buyArrestToken(account: 'Account', result: 'ServerResult', cost):
    if result and result.success:
        account.logger.info("花费%d金币, 购买抓捕令", cost)
