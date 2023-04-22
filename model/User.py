import logic.Format as Format
from logic.Config import config
from model.child import *  # noqa: F403
from model.enum.TaskType import TaskType
from model.enum.ActivityType import ActivityTypeString

SeasonString = ("", "春", "夏", "秋", "冬")

NationString = ("中立", "魏国", "蜀国", "吴国")

FormationString = ("不变阵", "鱼鳞阵", "长蛇阵", "锋矢阵", "偃月阵", "锥形阵", "八卦阵", "七星阵", "雁行阵")

ImposeEvent = ("金币", "征收", "民忠", "银币", "威望")  # 征收事件回答优先顺序


@wrapper  # noqa: F405
class User(BaseObject):  # noqa: F405
    """角色"""
    def __init__(self):
        super().__init__()
        self.playerid              = 0      # 角色id
        self.playername            = ""     # 角色名
        self.playerlevel           = 0      # 角色等级
        self.year                  = 0      # 年份
        self.season                = 0      # 季节
        self.nation                = 0      # 国家

        self.innewarea             = False  # 新区
        self.areaid                = 0      # 当前所在城池id
        self.areaname              = ""     # 当前所在城池名称
        self.spy_areaid            = 0      # 间谍所在城池id

        self.sys_gold              = 0      # 金币
        self.user_gold             = 0      # 充值金币
        self.jyungong              = 0      # 军功
        self.prestige              = 0      # 声望
        self.copper                = 0      # 银币
        self.food                  = 0      # 粮草
        self.forces                = 0      # 兵力
        self.bowlder               = 0      # 原石
        self.token                 = 0      # 军令
        self.atttoken              = 0      # 攻击令
        self.cityhp                = 0      # 城防值
        self.tickets               = 0      # 点券
        self.curactive             = 0      # 当前行动力

        self.magic                 = 0      # 强化成功率
        self.molistone             = 0      # 磨砺石
        self.maxtaozhuanglv        = 0      # 最大套装等级

        self.tokencd               = 0      # 军令冷却时间
        self.tokencdflag           = False  # 军令冷却状态
        self.transfercd            = 0      # 迁移冷却时间
        self.protectcd             = 0      # 保护冷却时间
        self.inspirecd             = 0      # 鼓舞冷却时间
        self.inspirestate          = 0      # 鼓舞状态
        self.rightcd               = 0      # 征义兵冷却时间
        self.rightnum              = 0      # 可征义兵次数

        self.maxcoin               = 0      # 银币上限
        self.maxfood               = 0      # 粮草上限
        self.maxforce              = 0      # 兵力上限
        self.maxbowlder            = 0      # 原石上限
        self.maxtoken              = 0      # 军令上限
        self.maxattacktoken        = 0      # 攻击令上限
        self.maxcityhp             = 0      # 城防值上限
        self.maxactive             = 0      # 行动力上限

        self.battlescore           = 0      # 战绩
        self.arreststate           = 0      # 劳作状态 0:正常 1:劳作 10:逃跑cd 100:被抓
        self.remainseniorslaves    = 0      # 剩余高级劳工(墨子改造)

        self.remaintutimes         = 0      # 屠城剩余次数
        self.tucd                  = 0      # 屠城冷却时间
        self.transfer_fail_num     = 0      # 移动失败次数

        self.area_map              = [      # 地图
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        self.astar                 = AreaAStar(self.area_map)  # A*算法 # noqa: F405

        self.warchariot            = False  # 战车
        self.canvisit              = False  # 恭贺争霸风云榜
        self.newtechnology         = False  # 科技
        self.cantech               = False  # 技术研究
        self.perdayreward          = False  # 今日手气
        self.version_gift          = False  # 版本更新奖励

        self.shenhuo                 = False  # 百炼精铁
        self.yuandanqifu             = False  # 酒神觉醒
        self.arrestevent             = False  # 抓捕活动
        self.boatevent               = False  # 龙舟
        self.cuilianevent            = False  # 淬炼大放送
        self.payhongbaoevent         = False  # 充值送红包
        self.bgevent                 = False  # 大宴群雄
        self.qingmingevent           = False  # 群雄煮酒
        self.duanwuevent             = False  # 百家宴
        self.moongeneralevent        = False  # 赏月送礼
        self.trainingevent           = False  # 大练兵
        self.snowtradingevent        = False  # 雪地通商
        self.bombnianevent           = False  # 抓年兽
        self.paradeevent             = False  # 阅兵庆典
        self.doubleelevenevent       = False  # 消费送礼
        self.memoryevent             = False  # 新春拜年
        self.towerstage              = False  # 宝塔活动
        self.goldboxevent            = False  # 群雄争霸
        self.nationdaygoldboxevent   = False  # 充值赠礼
        self.showkfwd                = False  # 武斗会
        self.showkfpvp               = False  # 英雄帖
        self.gifteventbaoshi4        = False  # 宝石翻牌
        self.dumpevent               = False  # 宝石倾销
        self.kfwdeventreward         = False  # 武斗庆典
        self.hasarchevent            = False
        self.baishen                 = False
        self.yang                    = False
        self.offlineevent            = False
        self.goldticketevent         = False
        self.yuebingevent            = False
        self.buffevent               = False
        self.moontowerevent          = False
        self.showkfyz                = False
        self.hasjailevent            = False
        self.feteevent               = False  # 祭祀活动
        self.borrowingarrowsevent    = False  # 草船借箭
        self.ringevent               = False  # 新年敲钟
        self.kfrank                  = True   # 对战
        self.eatmooncaketevent       = False  # 中秋月饼
        self.superfanpai             = False  # 超级翻牌
        self.springfestivalwishevent = False  # 许愿

        self.total_jailbaoshi                          = 0                 # 监狱劳作获得宝石
        self.imposedto                                 = ImposeDto()       # 征收  # noqa: F405
        self.generaltower                              = GeneralTower()    # 将军塔  # noqa: F405
        self.fengdi                                    = FengDi()          # 封地  # noqa: F405
        self.maincitydto: list[MainCityDto]            = BaseObjectList()  # 主城建筑  # noqa: F405
        self.constructordto: list[ConstructorDto]      = BaseObjectList()  # 建筑建造队列  # noqa: F405
        self.mozibuilding                              = BaseObjectList()  # 墨子建筑  # noqa: F405
        self.task: dict[TaskType, Task]                = BaseObjectDict()  # 日常任务  # noqa: F405
        self.ticket_exchange: dict[str, Ticket]        = BaseObjectDict()  # 点券兑换资源  # noqa: F405
        self.playerequipdto: dict[int, PlayerEquipDto] = BaseObjectDict()  # 套装  # noqa: F405
        self.tokenlist: list[Token]                    = BaseObjectList()  # 个人令 -1:未解锁 0:已使用 1:建造令 2:破坏令 3: 4:鼓舞令 5:诽谤令 6: 7:窃取令 8:战绩令 9:横扫令  # noqa: F405

    def get_available(self, key):
        value = getattr(self, key)
        reserve = config["global"]["reserve"].get(key, 0)
        return max(value - reserve, 0)

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

    def is_finish_task(self, task_type: TaskType):
        if (task := self.task.get(task_type)) is not None:
            return task.finishnum >= task.finishline
        return True

    def add_task_finish_num(self, task_type: TaskType, num: int) -> None:
        if (task := self.task.get(task_type)) is not None:
            task.finishnum += num

    def __repr__(self) -> str:
        return ", ".join((
            f"{self.playerlevel}级"
            f"{NationString[self.nation]}",
            f"{self.year}年{SeasonString[self.season]}",
            f"{self.gold}金币",
            f"{Format.GetShortReadable(self.copper)}银币",
            f"{Format.GetShortReadable(self.tickets)}点券",
            f"{self.curactive}行动力",
            f"{self.token}军令",
            f"{self.atttoken}攻击令",
            f"{self.cityhp}城防值",
            f"状态: {self.arreststate}",
        ))

    def HaveActivities(self):
        activities = []
        for k, v in ActivityTypeString.type2name.items():
            if getattr(self, k, False):
                activities.append(v)
        return ",".join(activities)

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
