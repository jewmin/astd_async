from model.child.BaseObject import wrapper, BaseObject


@wrapper
class GeneralTower(BaseObject):
    """将军塔"""
    def __init__(self):
        super().__init__()
        self.buildinggeneraltowernow = 0
        self.buildingprogress = 0
        self.leveluprequirement = 0
        self.buildingstone = 0
        self.gemstonenum = 0
        self.generaltowerlevel = 0
        self.addprogress = 0
        self.levelup = 0
