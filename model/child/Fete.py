from model.child.BaseObject import wrapper, BaseObject


@wrapper
class Fete(BaseObject):
    """祭祀"""
    def __init__(self):
        super().__init__()
        self.id = 0
        self.gold = 0
        self.name = ""
