import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("宴会")
async def getAllDinner(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "宴会期间": result.GetValue("indinnertime", 0) == 1,
            "已加入队伍": result.GetValue("teamstate", 0) == 1,
            "剩余宴会次数": result.GetValue("normaldinner.num", 0),
            "宴会队伍": [],
        }
        for team in result.GetValueList("team"):
            if team["num"] < team["maxnum"]:
                dict_info["宴会队伍"].append(team)
        return dict_info


@ProtocolMgr.Protocol("加入宴会队伍", ("teamId",))
async def joinDinner(account: 'Account', result: 'ServerResult', teamId, creator):
    if result and result.success:
        account.logger.info("加入宴会队伍[%s]", creator)
        return True
    return False
