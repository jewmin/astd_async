from model.child.BaseObject import wrapper, BaseObject


@wrapper
class FengDi(BaseObject):
    """封地"""

    def __init__(self):
        super().__init__()
        self.remainnum = 0  # 剩余封地生产次数
        self.freejiebinnum = 0  # 免费借兵次数
        self.jiebincost = 0  # 金币借兵消耗
        self.finish = 0  # 完成
        self.nextcd = 0  # 生产时间
