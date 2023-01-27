from model.child.BaseObject import wrapper, BaseObject, BaseObjectList
from model.child.GeneralTower import GeneralTower

SeasonString = ("", "春", "夏", "秋", "冬")

NationString = ("中立", "魏国", "蜀国", "吴国")

FormationString = ("不变阵", "鱼鳞阵", "长蛇阵", "锋矢阵", "偃月阵", "锥形阵", "八卦阵", "七星阵", "雁行阵")

ImposeEvent = ("金币", "征收", "民忠", "银币", "威望")  # 征收事件回答优先顺序


@wrapper
class User(BaseObject):
    """角色"""
    def __init__(self):
        super().__init__()
        self.playerid              = 0      # 角色id
        self.playername            = ""     # 角色名
        self.playerlevel           = 0      # 角色等级
        self.year                  = 0      # 年份
        self.season                = 0      # 季节
        self.nation                = 0      # 国家
        self.areaid                = 0      # 当前所在城池id
        self.areaname              = ""     # 当前所在城池名称
        self.sys_gold              = 0      # 金币
        self.user_gold             = 0      # 充值金币
        self.jyungong              = 0      # 军功
        self.prestige              = 0      # 声望
        self.copper                = 0      # 银币
        self.maxcoin               = 0      # 银币上限
        self.food                  = 0      # 粮草
        self.maxfood               = 0      # 粮草上限
        self.forces                = 0      # 兵力
        self.maxforce              = 0      # 兵力上限
        self.bowlder               = 0      # 原石
        self.maxbowlder            = 0      # 原石上限
        self.token                 = 0      # 军令
        self.maxtoken              = 0      # 军令上限
        self.maxattacktoken        = 0      # 攻击令上限
        self.cityhp                = 0      # 城防值
        self.maxcityhp             = 0      # 城防值上限
        self.curactive             = 0      # 当前行动力
        self.maxactive             = 0      # 行动力上限
        self.imposecd              = 0      # 征收冷却时间
        self.tokencd               = 0      # 军令冷却时间
        self.transfercd            = 0      # 迁移冷却时间
        self.protectcd             = 0      # 保护冷却时间
        self.inspirecd             = 0      # 鼓舞冷却时间
        self.inspirestate          = 0      # 鼓舞状态
        self.battlescore           = 0      # 战绩
        self.arreststate           = 0      # 劳作状态 0:正常 1:劳作 10:逃跑cd 100:被抓
        self.rightcd               = 0      # 征义兵冷却时间
        self.rightnum              = 0      # 可征义兵次数
        self.remainseniorslaves    = 0      # 剩余高级劳工(墨子改造)

        self.warchariot            = False  # 战车
        self.canvisit              = False  # 恭贺争霸风云榜
        self.newtechnology         = False  # 科技

        self.shenhuo               = False  # 百炼精铁
        self.yuandanqifu           = False  # 酒神觉醒
        self.arrestevent           = False  # 抓捕活动
        self.boatevent             = False  # 龙舟
        self.cuilianevent          = False  # 淬炼大放送
        self.payhongbaoevent       = False  # 充值送红包
        self.bgevent               = False  # 大宴群雄
        self.qingmingevent         = False  # 群雄煮酒
        self.duanwuevent           = False  # 百家宴
        self.moongeneralevent      = False  # 赏月送礼
        self.trainingevent         = False  # 大练兵
        self.snowtradingevent      = False  # 雪地通商
        self.bombnianevent         = False  # 抓年兽
        self.paradeevent           = False  # 阅兵庆典
        self.doubleelevenevent     = False  # 消费送礼
        self.memoryevent           = False  # 新春拜年
        self.towerstage            = False  # 宝塔活动
        self.goldboxevent          = False  # 群雄争霸
        self.nationdaygoldboxevent = False  # 充值赠礼
        self.showkfwd              = False  # 武斗会
        self.showkfpvp             = False  # 英雄帖
        self.gifteventbaoshi4      = False  # 宝石翻牌
        self.dumpevent             = False  # 宝石倾销
        self.kfwdeventreward       = False  # 武斗庆典
        self.hasarchevent          = False
        self.baishen               = False
        self.yang                  = False
        self.offlineevent          = False
        self.goldticketevent       = False
        self.yuebingevent          = False
        self.buffevent             = False
        self.moontowerevent        = False
        self.showkfyz              = False
        self.hasjailevent          = False

        self.innewarea             = False  # 新区
        self.imposecdflag          = False  # 征收冷却状态
        self.tokencdflag           = False  # 军令冷却状态
        self.cantech               = False  # 技术研究
        self.perdayreward          = False  # 今日手气
        self.version_gift          = False  # 版本更新奖励

        self.tickets               = 0      # 点券
        self.atttoken              = 0      # 攻击令
        self.total_jailbaoshi      = 0      # 监狱劳作获得宝石

        self.generaltower   = GeneralTower()    # 将军塔

        self.maincitydto    = BaseObjectList()  # 主城建筑
        self.constructordto = BaseObjectList()  # 建筑建造队列
        self.mozibuilding   = BaseObjectList()  # 墨子建筑

    @property
    def gold(self):
        return self.sys_gold + self.user_gold

    @staticmethod
    def get_impose_select_le(event1, event2):
        for event in ImposeEvent:
            if event in event1:
                return 1
            if event in event2:
                return 2

    @staticmethod
    def get_formation_by_name(formation: str) -> int:
        for idx, value in enumerate(FormationString):
            if formation == value:
                return idx

    @staticmethod
    def get_formation_by_id(formation_id: int) -> str:
        return FormationString[formation_id]

    def __repr__(self) -> str:
        return ", ".join((
            f"{self.playername}(id={self.playerid}, {self.playerlevel}级, {NationString[self.nation]})",
            f"{self.year}年{SeasonString[self.season]}",
            f"{self.gold}金币",
            f"{self.copper}银币",
            f"{self.tickets}点券",
            f"{self.curactive}行动力",
            f"{self.token}军令",
            f"{self.atttoken}攻击令",
            f"{self.cityhp}城防值",
            f"状态: {self.arreststate}",
        ))

    def HandleXml(self, info: dict) -> None:
        super().HandleXml(info)
        if "attacktoken" in info:
            self.atttoken = int(info["attacktoken"])
        if "jailbaoshi" in info:
            self.total_jailbaoshi += int(info["jailbaoshi"])

    def UpdatePlayerInfo(self, info: dict) -> None:
        self.HandleXml(info)

    def UpdatePlayerBattleInfo(self, info: dict) -> None:
        self.HandleXml(info)

    def RefreshPlayerInfo(self, info: dict) -> None:
        self.HandleXml(info)

    def UpdateLimits(self, info: dict) -> None:
        self.HandleXml(info)

    def UpdatePlayerExtraInfo(self, info: dict) -> None:
        self.HandleXml(info)

    def UpdatePlayerExtraInfo2(self, info: dict) -> None:
        self.HandleXml(info)

    def UpdateCityInfo(self, info: dict) -> None:
        self.HandleXml(info)

#     def set_task(self, list_task):
#         self.m_dictTasks = dict()
#         for task in list_task:
#             if task["taskstate"] == "1":
#                 t = Task()
#                 t.handle_info(task)
#                 self.m_dictTasks[t.type] = t

    # def add_task_finish_num(self, task_type, num):
    #     task = self.m_objUser.m_dictTasks.get(task_type, None)
    #     if task is not None:
    #         task.finishnum += num
