from model.child.BaseObject import wrapper, BaseObject
from model.child.RewardInfo import RewardInfo


@wrapper
class SpecialEquipCast(BaseObject):
    """铸造奖励"""

    def __init__(self):
        super().__init__()
        self.rewardinfo = RewardInfo()
