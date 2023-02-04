from model.child.BaseObject import wrapper, BaseObject
from model.child.RewardInfo import RewardInfo


@wrapper
class Task(BaseObject):
    """日常任务"""
    KEY = "type"

    def __init__(self):
        super().__init__()
        self.taskid = 0
        self.taskstate = 0
        self.taskname = ""
        self.content = ""
        self.finishnum = 0
        self.finishline = 0
        self.type = 0
        self.activity = 0
        self.rewardinfo = RewardInfo()
