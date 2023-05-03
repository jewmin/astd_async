import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("酒神觉醒")
async def getQifuEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "类型": result.GetValue("type"),
            "状态": result.GetValue("qifustate"),
            "福气": result.GetValue("fuqi"),
            "最大福气": result.GetValue("maxfuqi"),
            "本次祈福倍数": result.GetValue("xs"),
            "下次祈福倍数": result.GetValue("nextxs"),
            "祈福花费金币": result.GetValue("qifuneedcoin"),
            "全开花费金币": result.GetValue("fulingneedcoin"),
            "宝箱总福气": 0,
            "剩余的酒数量": 0,
        }
        for card in result.GetValueList("card"):
            info["宝箱总福气"] += card["fuqi"]
            if card["get"] == 0:
                info["剩余的酒数量"] += card["tickets"] * info["本次祈福倍数"]
        return info


@ProtocolMgr.Protocol("双倍祈福")
async def qifuActive(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("激活%d倍祈福", result.GetValue("xs"))


@ProtocolMgr.Protocol("选择祈福", ("indexId",))
async def qifuChoose(account: 'Account', result: 'ServerResult', indexId):
    if result and result.success:
        reward_info = RewardInfo(result.result["reward"]["rewardinfo"])  # noqa: F405
        account.logger.info("选择祈福[%s], 福气+%d, 获得%s", result.GetValue("reward.indexid"), result.GetValue("reward.fuqi"), reward_info)


@ProtocolMgr.Protocol("下一轮祈福")
async def nextQifu(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("进入下一轮祈福")


@ProtocolMgr.Protocol("开始祈福")
async def startQifu(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        account.logger.info("花费%d金币, 开始祈福", cost)


@ProtocolMgr.Protocol("金币全开")
async def qifuChooseAll(account: 'Account', result: 'ServerResult', cost=0):
    if result and result.success:
        account.logger.info("花费%d金币, 全开宝箱", cost)
