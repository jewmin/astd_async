import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
import protocol.mainCity as mainCity

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("获取系统时间")
async def getServerTime(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        server_time = int(result.result["time"])
        account.time_mgr.SetTimestamp(server_time)
        account.logger.debug("got timestamp = %d", server_time)


@ProtocolMgr.Protocol("获取玩家信息")
async def getPlayerInfoByUserId(account: 'Account', result: 'ServerResult', kwargs: dict):
    if not result.success:
        account.logger.warning("获取用户信息失败，请重试")
        return False

    if result.result.get("op") == "xzjs":
        code = result.result["code"]
        for player in result.result["player"]:
            if account.rolename == player["playername"]:
                playerId = player["playerid"]
                break
        else:
            account.logger.warning("您选择的角色不存在")
            return False

        if not await chooseRole(account, playerId=playerId, code=code):
            account.logger.warning("切换角色失败")
            return False

        return await getPlayerInfoByUserId(account)

    if "blockreason" in result.result:
        account.logger.warning("角色被封号，原因是：%s", result.result["blockreason"])
        return False

    if "player" in result.result:
        account.user.RefreshPlayerInfo(result.result["player"])
    else:
        account.user.RefreshPlayerInfo(result.result["message"]["player"])

    if "limitvalue" in result.result:
        account.user.UpdateLimits(result.result["limitvalue"])
    else:
        account.user.UpdateLimits(result.result["message"]["limitvalue"])

    if account.user.version_gift:
        await mainCity.getUpdateReward(account)

    account.logger.info(account.user)
    return True


@ProtocolMgr.Protocol("选择玩家角色", ("playerId", "code"))
async def chooseRole(account: 'Account', result: 'ServerResult', kwargs: dict):
    return result.success


@ProtocolMgr.Protocol("获取额外信息")
async def getExtraInfo(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.UpdatePlayerExtraInfo(result.result["player"])


@ProtocolMgr.Protocol("获取玩家额外信息")
async def getPlayerExtraInfo2(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.UpdatePlayerExtraInfo2(result.result["player"])
