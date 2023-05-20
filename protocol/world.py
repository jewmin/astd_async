import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("世界")
async def getNewArea(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.user.astar.ignore_barrier(False)
        account.user.fengdi.HandleXml(result.result["fengdi"])
        dict_info = {
            "决斗战旗": result.GetValue("daoju.flagnum"),
            "诱敌锦囊": result.GetValue("daoju.jinnum"),
            "城防恢复cd": result.GetValue("cityhprecovercd"),
            "免费移动次数": result.GetValue("freeclearmovetime"),
            "移动cd": result.GetValue("tranfercd"),
            "悬赏目标": result.GetValue("targetid", 0),
            "悬赏目标城池": result.GetValue("targetareaid", 0),
            "悬赏目标城区": result.GetValue("targetscopeid", 0),
            "穿越": result.GetValue("achfree", 0) == 1,
            "所有城池": {},
            "封地城池": {},
            "城池ID": {},
            "城池名": {},
        }

        for area in result.GetValueList("newarea"):
            # coordinate = list(map(int, area["coordinate"].split(",")))
            coordinate = area["coordinate"]
            y, x = coordinate[0] - 1, coordinate[1] - 1
            if "areaid" in area:
                areaid = area["areaid"]
                if area.get("isselfarea", 0) == 1:
                    account.user.areaid = areaid
                if area.get("ziyuan", 0) == 100:
                    account.user.spy_areaid = areaid
                if area.get("fengdiflag", "") != "" and area["nation"] == account.user.nation:
                    dict_info["封地城池"][areaid] = area
                dict_info["城池ID"][areaid] = area
                dict_info["城池名"][area["areaname"]] = area
                dict_info["所有城池"][(y, x)] = area

        return dict_info


@ProtocolMgr.Protocol("迁移")
async def getTranferInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        if result.GetValue("canget", 0) == 1:
            await getTransferToken(account)


@ProtocolMgr.Protocol("领取攻击令")
async def getTransferToken(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取攻击令, 攻击令+%d", result.GetValue("token", 0))


@ProtocolMgr.Protocol("移动", ("areaId",))
async def transferInNewArea(account: 'Account', result: 'ServerResult', areaId, area):
    if result.success:
        account.logger.info("移动, 城池[%s]", area["areaname"])
        return True
    else:
        account.logger.warning("移动, 城池[%s], 失败: %s", area["areaname"], result.error)
        return False


@ProtocolMgr.Protocol("清除移动冷却时间")
async def cdMoveRecoverConfirm(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("清除移动冷却时间")


@ProtocolMgr.Protocol("屠城嘉奖")
async def getTuCityInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        if result.GetValue("recvednum", 0) < result.GetValue("maxrecvednum", 0):
            for info in result.GetValueList("info"):
                await getTuCityReward(account, playerId=info["playerid"], areaId=info["areaid"])


@ProtocolMgr.Protocol("搜刮屠城嘉奖", ("playerId", "areaId"))
async def getTuCityReward(account: 'Account', result: 'ServerResult', playerId, areaId):
    if result.success:
        account.logger.info("搜刮屠城嘉奖, %s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("屠城", ("areaId",))
async def tuCity(account: 'Account', result: 'ServerResult', areaId):
    if result.success:
        account.logger.info("屠城, 宝石+%d", result.GetValue("baoshi", 0))


@ProtocolMgr.Protocol("个人令")
async def getNewAreaToken(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.user.tokenlist.HandleXml('token', result.result["tokenlist"])
        account.user.remaintutimes = result.GetValue("tucity.remaintutimes", 0)
        account.user.tucd = result.GetValue("tucity.tucd", 0)


@ProtocolMgr.Protocol("使用建造令", ("newTokenId",))
async def useConstuctToken(account: 'Account', result: 'ServerResult', newTokenId):
    if result.success:
        account.logger.info("使用建造令lv.%d, 城防+%d", result.GetValue("tokenlevel", 0), result.GetValue("effect", 0))


@ProtocolMgr.Protocol("使用战绩令", ("newTokenId",))
async def useScoreToken(account: 'Account', result: 'ServerResult', newTokenId):
    if result.success:
        account.logger.info("使用战绩令lv.%d", result.GetValue("tokenlevel", 0))


@ProtocolMgr.Protocol("使用鼓舞令", ("newTokenId",))
async def useInspireToken(account: 'Account', result: 'ServerResult', newTokenId):
    if result.success:
        account.logger.info("使用鼓舞令lv.%d", result.GetValue("tokenlevel", 0))


async def useToken(account: 'Account', token: Token):  # noqa: F405
    if token.tokenid == 1:
        await useConstuctToken(account, newTokenId=token.id)
    elif token.tokenid == 4:
        await useInspireToken(account, newTokenId=token.id)
    elif token.tokenid == 8:
        await useScoreToken(account, newTokenId=token.id)
    else:
        account.logger.warning("未知个人令[%s]", token)


@ProtocolMgr.Protocol("战绩")
async def getBattleRankingInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "宝箱": result.GetValue("box", 0),
            "上轮战绩排名奖励": result.GetValue("lastrankingreward", 0) != 0,
            "已领取上轮战绩排名奖励": result.GetValue("getlast") == 1,
            "战绩奖励": result.GetValueList("scorerewardinfo.rinfo"),
        }
        return dict_info


@ProtocolMgr.Protocol("领取战绩奖励", ("pos",))
async def getBattleScoreReward(account: 'Account', result: 'ServerResult', pos):
    if result.success:
        account.logger.info("领取战绩奖励, 宝石+%d, 宝箱+%d", result.GetValue("baoshi", 0), result.GetValue("box", 0))


@ProtocolMgr.Protocol("打开战绩宝箱")
async def openScoreBox(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("打开战绩宝箱, %s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("领取上轮战绩排名奖励")
async def getBattleRankReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取上轮战绩排名奖励, 宝石+%d", result.GetValue("baoshi", 0))


@ProtocolMgr.Protocol("领取封地奖励")
async def recvFengdiReward(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取封地奖励, %s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405
        account.user.fengdi.HandleXml(result.result["fengdi"])
    else:
        account.user.fengdi.finish = 0


@ProtocolMgr.Protocol("封地资源列表", ("areaId",))
async def generateBigG(account: 'Account', result: 'ServerResult', areaId):
    if result.success:
        for produceinfo in result.GetValueList("produceinfo"):
            if produceinfo["resid"] == 4:
                await startProduce(account, areaId=areaId, resId=4, produceinfo=produceinfo)
                break


@ProtocolMgr.Protocol("封地生产资源", ("areaId", "resId"))
async def startProduce(account: 'Account', result: 'ServerResult', areaId, resId, produceinfo):
    if result.success:
        res_list = {
            1: "宝石",
            2: "镔铁",
            3: "兵器",
            4: f"大将令({produceinfo['bigname']})",
            5: "觉醒酒",
        }
        account.logger.info("封地生产资源[%s]", res_list[resId])


@ProtocolMgr.Protocol("悬赏")
async def getNewCityEventInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        dict_info = {
            "悬赏任务列表": [],
            "悬赏星数奖励": result.GetValueList("starreward"),
            "悬赏剩余次数": result.GetValue("remaintimes", 0),
            "悬赏剩余时间": result.GetValue("taskremaintime", 0),
            "悬赏已完成": result.GetValue("taskstate", 0) == 1,
        }
        tasks = result.GetValue("taskstr").split(",")
        for pos, task in enumerate(tasks, 1):
            if task:
                content = list(map(int, task.split(":")))
                if content[1] == 0:
                    dict_info["悬赏任务列表"].append({"位置": pos, "星级": content[0]})
        dict_info["悬赏任务列表"] = sorted(dict_info["悬赏任务列表"], key=lambda x: x["星级"], reverse=True)
        return dict_info


@ProtocolMgr.Protocol("领取悬赏星数奖励", ("pos",))
async def recvNewCityEventStarReward(account: 'Account', result: 'ServerResult', pos):
    if result.success:
        account.logger.info("领取悬赏星数奖励, %s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("领取悬赏任务", ("pos",))
async def acceptNewCityEvent(account: 'Account', result: 'ServerResult', pos, task):
    if result.success:
        account.logger.info("领取%d星悬赏任务", task["星级"])


@ProtocolMgr.Protocol("领取悬赏奖励")
async def deliverNewCityEvent(account: 'Account', result: 'ServerResult'):
    if result.success:
        account.logger.info("领取悬赏奖励, %s", RewardInfo(result.result["rewardinfo"]))  # noqa: F405


@ProtocolMgr.Protocol("国家宝箱")
async def getNewAreaTreasureInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        return result.GetValue("treasurenum", 0)
    return 0


@ProtocolMgr.Protocol("连开5个国家宝箱")
async def draw5NewAreaTreasure(account: 'Account', result: 'ServerResult'):
    if result.success:
        t2n = {
            1: "银币",
            2: "攻击令",
            3: "军令",
            4: "玉石",
            5: "点券",
            6: "宝石",
            7: "专属家传玉佩",
            8: "点券",
        }
        rs = {}
        for reward in result.GetValueList("reward"):
            t = reward["rewardtype"]
            if t in (1, 2, 3, 4, 5, 6):
                rs[t] = rs.get(t, 0) + reward["rewardvalue"]
            if (baowu := reward.get("baowu", 0)) > 0:
                rs[7] = rs.get(7, 0) + baowu
            if (tickets := reward.get("tickets", 0)) > 0:
                rs[8] = rs.get(8, 0) + tickets
        account.logger.info("连开5个国家宝箱, %s", ", ".join(f"{t2n[k]}+{v}" for k, v in rs.items()))


@ProtocolMgr.Protocol("攻击敌人", ("areaId", "scopeId", "cityId"))
async def attackOtherAreaCity(account: 'Account', result: 'ServerResult', areaId, scopeId, cityId):
    if result.success:
        if result.GetValue("worldevent", 0) == 1:
            account.user.spy_areaid = account.user.areaid

        arrest_state = result.GetValue("slavename", "") != ""
        attack_back = result.GetValue("rewardattackbacktimes", "") != ""
        winside = True
        if "battlereport" in result.result:
            winside = result.GetValue("battlereport.winside", 0)
            de = {"名称": result.GetValue("defender.playername"), "等级": result.GetValue("defender.playerlevel")}
            report = {
                "战绩": result.GetValue("battlereport.attscore"),
                "消息": result.GetValue("battlereport.message"),
                "城防": [result.GetValue("battlereport.attcityhpchange"), result.GetValue("battlereport.defcityhpchange")],
                "胜负": "胜利" if winside else "失败",
            }
        else:
            de = {"名称": "禁卫军", "等级": account.user.playerlevel}
            if result.GetValue("myspy", 0) != 0:
                de["名称"] = "间谍"
            elif result.GetValue("defender.playertype", 0) == 3:
                de["名称"] = "守备军"
            report = {
                "战绩": result.GetValue("attscore"),
                "消息": "",
                "城防": [result.GetValue("attcityhpchange"), result.GetValue("defcityhpchange")],
                "胜负": "胜利",
            }
        account.logger.info("您攻打%s, %s, %s, 战绩+%d, 您/敌(%d级)城防减少%d/%d", de["名称"], report["胜负"], report["消息"], report["战绩"], de["等级"], report["城防"][0], report["城防"][1])
        if winside:
            return True, "", arrest_state, attack_back
        else:
            return False, "打不过敌人", arrest_state, attack_back

    account.logger.warning("攻击敌人[areaid=%d, scopeid=%d, cityid=%d]失败: %s", areaId, scopeId, cityId, result.error)
    return False, result.error, False, False


@ProtocolMgr.Protocol("决斗", ("areaId", "scopeId", "cityId", "type"))
async def useWorldDaoju(account: 'Account', result: 'ServerResult', areaId, scopeId, cityId, type, desc, city):
    if result.success:
        account.logger.info("对玩家[%s]%s", city["playername"], desc)
        toareaid = result.GetValue("toareaid", 0)
        toscopeid = result.GetValue("toscopeid", 0)
        toplayerid = result.GetValue("toplayerid", 0)
        return True, {"城池": toareaid, "区域": toscopeid, "玩家": toplayerid}, ""

    account.logger.info("对玩家[%s]%s, 失败: %s", city["playername"], desc, result.error)
    return False, None, result.error


@ProtocolMgr.Protocol("决斗信息", ("type",))
async def getPkInfo(account: 'Account', result: 'ServerResult', type):
    if result.success:
        pk_info = {
            "阶段": result.GetValue("stage"),
            "结果": result.GetValue("pkresult"),
            "剩余时间": result.GetValue("remaincd", 0),
            "防": {
                "城防": result.GetValue("fang.cityhp"),
                "最大城防": result.GetValue("fang.maxcityhp"),
                "玩家": result.GetValue("fang.name"),
            },
            "攻": {
                "城防": result.GetValue("gong.cityhp"),
                "最大城防": result.GetValue("gong.maxcityhp"),
                "玩家": result.GetValue("gong.name"),
            },
            "目标": {
                "城池": result.GetValue("pkinfo.areaid", 0),
                "区域": result.GetValue("pkinfo.scopeid", 0),
                "城市": result.GetValue("pkinfo.cityid", 0),
            }
        }
        return pk_info
