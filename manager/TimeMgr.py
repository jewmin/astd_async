import time
import pytz
from datetime import datetime


class TimeMgr:
    """时间管理"""
    def __init__(self):
        self.offset = 0

    def SetTimestamp(self, timestamp: int) -> None:
        """设置服务器偏移时间, 单位: 毫秒"""
        self.offset = int(round(time.time() * 1000)) - timestamp

    def GetTimestamp(self) -> int:
        """获取服务器时间, 单位: 毫秒"""
        return int(round(time.time() * 1000)) - self.offset

    def GetTime(self) -> float:
        """获取服务器时间, 单位: 秒"""
        return self.GetTimestamp() / 1000

    def GetDatetime(self) -> datetime:
        """year, month, day, hour, minute, second, microsecond"""
        return datetime.fromtimestamp(self.GetTimestamp() / 1000, pytz.timezone("UTC"))

    @staticmethod
    def GetDatetimeString(microseconds: int) -> str:
        dt = datetime.fromtimestamp(microseconds / 1000, pytz.timezone("UTC"))
        return f"{dt.hour}:{dt.minute}:{dt.second}"
