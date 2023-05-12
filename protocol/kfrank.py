import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("乱世风云榜")
async def getMatchDetail(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "花费军令": result.GetValue("message.needtoken"),
            "可领取上届排名奖励": result.GetValue("message.boxinfo.havegetlast") == 0,
            "对战可领取宝箱": result.GetValue("message.boxinfo.canget") == 1,
            "拥有宝箱": result.GetValue("message.boxinfo.boxnum"),
            "任务": result.GetValue("message.taskinfo"),
            "对战状态": result.GetValue("message.status"),
            "状态": result.GetValue("message.globalstate"),
            "准备状态": result.GetValue("message.canready", 0) == 1,
            "下次战斗冷却时间": result.GetValue("message.nextbattlecd"),
            "排名": 0,
            "积分": 0,
        }
        for player_info in result.GetValue("message.selfrank.playerinfo"):
            if player_info.get("self", 0) == 1:
                info["排名"] = player_info["rank"]
                info["积分"] = player_info["score"]
                break
        return info


@ProtocolMgr.Protocol("匹配对手")
async def startMatch(account: 'Account', result: 'ServerResult', token):
    if result.success:
        account.logger.info("花费%d军令, 匹配对手", token)


@ProtocolMgr.Protocol("准备就绪")
async def ready(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("准备就绪")


@ProtocolMgr.Protocol("同步阵型")
async def syncData(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("同步阵型")


@ProtocolMgr.Protocol("刷新对战任务")
async def changeTask(account: 'Account', result: 'ServerResult'):
    if result.success:
        task_info = result.GetValue("message.taskinfo")
        account.logger.info("刷新对战任务, 新任务[%s - %s(宝箱+%d)]", task_info["name"], task_info["intro"], task_info["reward"])
        return task_info


@ProtocolMgr.Protocol("打开对战宝箱")
async def openBox(account: 'Account', result: 'ServerResult'):
    if result.success:
        msg = ["打开对战宝箱"]
        if "tickets" in result.result["message"]:
            msg.append(f"获得点券+{result.GetValue('message.tickets.num')}")
        if "rewardgeneral" in result.result["message"]:
            msg.append(f"获得大将令[{result.GetValue('message.rewardgeneral.name')}]+{result.GetValue('message.rewardgeneral.num')}")
        account.logger.info(", ".join(msg))


@ProtocolMgr.Protocol("领取对战任务奖励")
async def recvTaskReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取对战任务奖励, 获得宝箱+%d", result.GetValue("message.boxnum"))


@ProtocolMgr.Protocol("领取对战上届排名奖励")
async def recvLastReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取对战上届排名奖励, 获得宝箱+%d", result.GetValue("message.boxreward"))
