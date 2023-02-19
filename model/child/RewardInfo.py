from model.child.BaseObject import wrapper, BaseObject, BaseObjectList
import logic.Format as Format

RewardString = (
    "type:0", "银币", "玉石", "type:3", "type:4", "宝石", "兵器", "兵器碎片", "征收次数", "纺织次数",
    "通商次数", "炼化次数", "兵力减少", "副本重置卡", "战役双倍卡", "强化暴击卡", "强化打折卡", "兵器提升卡", "兵器暴击卡", "type:19",
    "type:20", "type:21", "type:22", "type:23", "type:24", "攻击令", "type:26", "进货令", "军令", "政绩翻倍卡",
    "征收翻倍卡", "商人召唤卡", "纺织翻倍卡", "type:33", "行动力", "摇钱树", "超级门票", "type:37", "宝物", "金币",
    "type:40", "type:41", "点券", "神秘宝箱", "家传玉佩", "type:45", "type:46", "type:47", "铁锤", "大将令",
    "镔铁", "专属装备", "type:52", "type:53", "type:54", "type:55", "觉醒酒", "磨砺石", "紫晶石", "1亿点券",
    "筑造石", "type:61", "杜康酒", "type:63", "精魄", "type:65", "type:66", "type:67", "type:68", "type:69",
    "type:70", "type:71", "type:72", "type:73", "type:74", "type:75", "type:76", "type:77", "type:78", "type:79",
)


@wrapper
class RewardInfo(BaseObject):
    """奖励"""
    def __init__(self, info: dict = None):
        super().__init__()
        self.reward: list['Reward'] = BaseObjectList()
        self.HandleXml(info)

    def __repr__(self) -> str:
        rewards = []
        for reward in self.reward:
            rewards.append(repr(reward))
        return " ".join(rewards)


@wrapper
class Reward(BaseObject):
    def __init__(self):
        super().__init__()
        self.type = 0
        self.itemname = ""
        self.quality = 0
        self.lv = 0
        self.num = 0

    def __repr__(self) -> str:
        return f"{RewardString[self.type]}(lv.{self.lv})+{Format.GetShortReadable(self.num)}"
