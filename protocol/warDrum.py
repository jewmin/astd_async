import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("战鼓")
async def getWarDrumInfo(account: 'Account', result: 'ServerResult'):
    if result and result.success:
        dict_info = {
            "最大等级": result.GetValue("maxupdatelevel"),
            "库存点券": result.GetValue("ticketnum"),
            "库存玉石": result.GetValue("bowldernum"),
            "库存镔铁": result.GetValue("steelnum"),
            "最大战鼓等级": 0,
            "最小战鼓等级": 999,
            "战鼓列表": {},
        }
        for war_drum in result.GetValueList("getwardruminfo.wardrum"):
            war_drum_info = {
                "名称": war_drum["name"],
                "类型": war_drum["type"],
                "当前等级": war_drum["drumlevel"],
                "特殊等级": war_drum["speciallevel"],
                "最大特殊等级": war_drum["maxspeciallevel"],
                "消耗镔铁": war_drum["needsteelnum"],
                "消耗玉石": war_drum["needbowldernum"],
                "消耗点券": war_drum["needticketnum"],
                "当前进度": war_drum["effectnum"],
                "总进度": war_drum["totalnum"],
                "高效": war_drum["needdouble"] == 1,
            }
            dict_info["战鼓列表"][war_drum_info["类型"]] = war_drum_info
            dict_info["最大战鼓等级"] = max(dict_info["最大战鼓等级"], war_drum_info["当前等级"])
            dict_info["最小战鼓等级"] = min(dict_info["最小战鼓等级"], war_drum_info["当前等级"])
        dict_info["最大等级差"] = dict_info["最大战鼓等级"] - dict_info["最小战鼓等级"]
        return dict_info


@ProtocolMgr.Protocol("强化战鼓", ("type",))
async def strengthenWarDrum(account: 'Account', result: 'ServerResult', type, steelnum, bowldernum, ticketnum):
    if result and result.success:
        dict_info = {
            "战鼓": result.GetValue("wardrumdto.name", ""),
            "当前进度": result.GetValue("wardrumdto.effectnum", 0),
            "总进度": result.GetValue("wardrumdto.totalnum", 0),
            "进度": result.GetValue("crits", 0),
            "余料": result.GetValue("surplus", 0),
        }
        if dict_info["当前进度"] == 0:
            msg = "战鼓升级"
        else:
            msg = f"强化战鼓[{dict_info['战鼓']}], 消耗镔铁-{steelnum}, 玉石-{bowldernum}, 点券-{ticketnum}, 进度+{dict_info['进度']}, {dict_info['当前进度']}/{dict_info['总进度']}, 余料+{dict_info['余料']}"
        account.logger.info(msg)
        return True
