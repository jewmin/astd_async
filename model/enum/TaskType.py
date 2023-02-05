from enum import Enum, unique


@unique
class TaskType(Enum):
    """任务类型"""
    Impose      = 1  # 征收
    ForceImpose = 2  # 强征
