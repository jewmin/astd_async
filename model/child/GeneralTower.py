from model.child.BaseObject import wrapper, BaseObject


@wrapper
class GeneralTower(BaseObject):
    """将军塔"""
    def __init__(self):
        super().__init__()
        self.buildinggeneraltowernow = 0
        self.generaltowerlevel = 0
