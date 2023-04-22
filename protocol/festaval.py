import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
from logic.Format import GetShortReadable

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("宝塔活动")
async def getTowerEventInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        info = {
            "阶段": result.GetValue("stage"),
            "选中宝塔": result.GetValue("curtowerid", 0),
            "宝塔": result.GetValue("towerbaoshi"),
            "宝石": result.GetValue("curbaoshi", 0),
            "状态": result.GetValue("curstate", -1),
        }
        return info


async def doAcceptByTowerId(account: 'Account', tower):
    await acceptByTowerId(account, towerId=tower["id"], tower=tower)


@ProtocolMgr.Protocol("选择宝塔", ("towerId",))
async def acceptByTowerId(account: 'Account', result: 'ServerResult', towerId, tower):
    if result and result.success:
        account.logger.info("选择宝塔[%s], 要求: %s宝石, 奖励: %s宝石 %d筑造石", tower["name"], GetShortReadable(tower["baoshi"]), GetShortReadable(tower["reward"]), tower["rewardbuildingstone"])


@ProtocolMgr.Protocol("完成宝塔")
async def finishTower(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = 1
        reward.num = result.GetValue("baoshi")
        reward_info.reward.append(reward)
        account.logger.info("完成宝塔，获得筑造石+%d, %s", result.GetValue("buildingstone"), reward_info)
