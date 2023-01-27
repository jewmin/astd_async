from model.child.BaseObject import wrapper, BaseObject


@wrapper
class MoZiBuilding(BaseObject):
    """墨子建筑"""
    def __init__(self):
        super().__init__()
        self.id = 0
        self.buildid = 0
        self.slaves = 0
        self.process = 0
        self.state = 0
        self.totalprocess = 0
        self.lv = 0
        self.seniorprocess = 0
        self.totalseniorprocess = 0
        self.canupgrade = 0
        self.intro = ""
