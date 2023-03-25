from model.child.BaseObject import wrapper, BaseObject


@wrapper
class Token(BaseObject):
    """个人令"""

    def __init__(self):
        super().__init__()
        self.id = 0
        self.tokenid = 0
        self.name = ""
        self.level = 0

    def __repr__(self) -> str:
        return f"{self.tokenid}_{self.name}_{self.level}"
