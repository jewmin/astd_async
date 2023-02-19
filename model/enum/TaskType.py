from enum import IntEnum, unique


@unique
class TaskType(IntEnum):
    """任务类型"""
    Impose      = 1  # 征收
    ForceImpose = 2  # 强征
    FeteGem     = 3  # 宝石祭祀
    BigFete     = 4  # 大祭祀
