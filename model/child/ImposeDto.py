from model.child.BaseObject import wrapper, BaseObject


@wrapper
class ImposeDto(BaseObject):
    """征收"""
    def __init__(self):
        super().__init__()
        self.imposenum = 0
        self.imposemaxnum = 0
        self.forceimposecost = 0
        self.cdflag = False
        self.lastimposetime = 0
