import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("王朝寻宝")
async def getNewTreasureGameInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dice_num = result.GetValue("dicenum", 0)
        account.logger.info("王朝寻宝, 当前骰子: %d", dice_num)
        return dice_num


@ProtocolMgr.Protocol("开始探宝")
async def startNewTGame(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        dict_info = {
            "当前骰子": result.GetValue("dicenum", 0),
            "可购买骰子": result.GetValue("golddicenum", 0),
            "购买骰子消耗金币": result.GetValue("buycost", 999),
            "可购买次数": result.GetValue("havebuytimes", 0),
            "当前位置": result.GetValue("curpos", 0),
            "事件位置": result.GetValue("eventpos", 0),
            "剩余步数": result.GetValue("remainnum", 0),
            "当前地图": result.GetValue("curmapid", 0),
            "下一地图": result.GetValue("nextmapid", 0),
            "换地图": result.GetValue("changemap", 0) == 1,
            "探宝完毕": result.GetValue("needfinish", 0) == 1,
        }
        if "eventtype" in result.result:
            _handle_treasure_event(dict_info, result.result)
        account.logger.info("当前骰子: %d", dict_info["当前骰子"])
        return dict_info


def _handle_treasure_event(dict_info: dict, result: dict):
    event_type = int(result["eventtype"])
    dict_info["事件"] = event_type
    if event_type == 1:
        dict_info["探索路径步数"] = int(result["footnum"])
        dict_info["事件名称"] = f"[探索路径]事件，行走了{dict_info['探索路径步数']}步"

    elif event_type == 2:
        dict_info["免费摇摇钱树"] = int(result["freeshake"])
        dict_info["下一次宝石奖励"] = RewardInfo(result["nextbaoshi"]["rewardinfo"])  # noqa: F405
        dict_info["事件名称"] = f"[摇钱树]事件，下一次宝石奖励[{dict_info['下一次宝石奖励']}]"

    elif event_type == 3:
        dict_info["购买宝箱消耗金币"] = int(result["goldboxcost"])
        dict_info["购买宝箱"] = result["rewardname"]
        dict_info["事件名称"] = f"[购买宝箱]事件，宝箱[{dict_info['购买宝箱']}({dict_info['购买宝箱消耗金币']}金币)]"


@ProtocolMgr.Protocol("执行探宝事件", ("open",))
async def handlerEvent(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        msg = kwargs["msg"]
        if "rewardinfo" in result.result:
            msg += f", 获得{RewardInfo(result.result['rewardinfo'])}"  # noqa: F405
        account.logger.info(msg)


@ProtocolMgr.Protocol("掷骰子")
async def useNewTDice(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        msg = f"掷到{result.GetValue('movenum')}点"
        if "pointreward" in result.result:
            msg += f", {_handle_point_reward(result.result['pointreward'])}"
        account.logger.info(msg)


def _handle_point_reward(point_reward_list: list):
    if not isinstance(point_reward_list, list):
        point_reward_list = [point_reward_list]

    msg_list = []
    for point_reward in point_reward_list:
        if "eventtype" in point_reward:
            dict_info = {}
            _handle_treasure_event(dict_info, point_reward)
            msg_list.append(f"发现{dict_info['事件名称']}")
        if "rewardinfo" in point_reward:
            msg_list.append(f"获得{RewardInfo(point_reward['rewardinfo'])}")  # noqa: F405

    return ", ".join(msg_list)


@ProtocolMgr.Protocol("换地图")
async def transfer(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        msg = "更换寻宝地图"
        if "pointreward" in result.result:
            msg += f", {_handle_point_reward(result.result['pointreward'])}"
        account.logger.info(msg)


@ProtocolMgr.Protocol("探宝完毕")
async def awayNewTGame(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result and result.success:
        account.logger.info("探宝完毕")
