from model.child.BaseObject import wrapper, BaseObject


@wrapper
class MainCityDto(BaseObject):
    """主城建筑"""
    def __init__(self):
        super().__init__()
        self.id = 0
        self.buildid = 0
        self.buildname = ""
        self.intro = ""
        self.buildlevel = 0
        self.nextcopper = 0
        self.cdtime = 0
        self.lastcdtime = 0
        self.lastupdatetime = 0
