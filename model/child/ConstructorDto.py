from model.child.BaseObject import wrapper, BaseObject


@wrapper
class ConstructorDto(BaseObject):
    """建筑建造队列"""
    def __init__(self):
        super().__init__()
        self.cid = 0
        self.cdflag = 0
        self.ctime = 0
