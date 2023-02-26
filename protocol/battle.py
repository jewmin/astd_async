import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("征战", sub_module=False)
async def battle(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "征战事件": result.GetValue("battleevent", {}),
            "免费强攻令": result.GetValue("freeattnum", 0),
        }
        return dict_info


@ProtocolMgr.Protocol("强攻NPC", ("armyId",))
async def forceBattleArmy(account: 'Account', result: 'ServerResult', armyId):
    if result and result.success:
        account.logger.info(
            "强攻NPC, %s, 你损失兵力%s, 敌方损失兵力%s",
            result.GetValue("battlereport.message"),
            result.GetValue("battlereport.attlost"),
            result.GetValue("battlereport.deflost"),
        )


@ProtocolMgr.Protocol("征战NPC", ("armyId",))
async def battleArmy(account: 'Account', result: 'ServerResult', armyId):
    if result and result.success:
        account.logger.info(
            "征战NPC, %s, 你损失兵力%s, 敌方损失兵力%s",
            result.GetValue("battlereport.message"),
            result.GetValue("battlereport.attlost"),
            result.GetValue("battlereport.deflost"),
        )


@ProtocolMgr.Protocol("进行征战事件")
async def doBattleEvent(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        if process := result.GetValue("battleevent.process"):
            account.logger.info("进行征战事件: %s", process)
        else:
            account.logger.info("进行征战事件: 完毕")


@ProtocolMgr.Protocol("领取征战事件奖励")
async def recvBattleEventReward(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        account.logger.info("领取征战事件奖励, 获得%s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("征战地图", ("powerId",))
async def getPowerInfo(account: 'Account', result: 'ServerResult', powerId):
    if result and result.success:
        return result.GetValue("army")
