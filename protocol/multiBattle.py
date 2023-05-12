import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("加入征战军团", ("teamId",))
async def joinTeam(account: 'Account', result: 'ServerResult', teamId):
    if result.success:
        account.logger.info("加入征战军团[%s]", teamId)


@ProtocolMgr.Protocol("征战军团", ("armiesId",))
async def getTeamInfo(account: 'Account', result: 'ServerResult', armiesId):
    if result.success:
        if teams := result.GetValueList("team"):
            teamid = teams[0]["teamid"]
            account.user.teamid = teamid
            account.user.armiesId = armiesId
            await joinTeam(account, teamId=teamid)
            return teamid
