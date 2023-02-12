import asyncio
import datetime
from weakref import proxy
from logic.Config import config
import manager.ProtocolMgr as ProtocolMgr

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from manager.TaskMgr import TaskMgr
    from model.Account import Account


class BaseTask:
    """任务基类"""
    def __init__(self, account):
        self.name = "任务名称"
        self.task_mgr: TaskMgr = None
        self.account: Account = proxy(account)
        self.task: asyncio.Task = None

    def Cancel(self, msg=None):
        if not self.task:
            return
        self.task.cancel(msg)
        self.task = None

    def Run(self):
        self.task = asyncio.get_event_loop().create_task(self._Run())

    async def _Exec(self):
        raise NotImplementedError("必须实现此函数")

    async def _Run(self):
        if not self.account.running:
            self.task_mgr.StopAllTasks("停止挂机")
            return

        try:
            next_running_time = await self._Exec()
        except ProtocolMgr.ProtocolError as ex:
            self.account.logger.error(ex)
            next_running_time = self.next_half_hour
        except ProtocolMgr.ReloginError as ex:
            self.account.logger.error(ex)
            self.account.running = False
            self.account.Relogin(1800)
        except Exception:
            self.account.logger.LogLastExcept()
            next_running_time = self.next_half_hour

        if not self.account.running:
            self.task_mgr.StopAllTasks("停止挂机")
            return

        asyncio.get_event_loop().call_later(next_running_time, self.Run)

    def get_available(self, key):
        value = getattr(self.account.user, key)
        reserve = config["global"]["reserve"].get(key, 0)
        return max(value - reserve, 0)

    @property
    def immediate(self) -> int:
        """马上"""
        return 2

    @property
    def one_minute(self) -> int:
        return 60

    @property
    def two_minute(self) -> int:
        return 120

    @property
    def ten_minute(self) -> int:
        return 600

    @property
    def half_hour_later(self) -> int:
        return 1800

    @property
    def an_hour_later(self) -> int:
        return 3600

    @property
    def next_half_hour(self) -> int:
        """下一个整半小时"""
        if (remainder := 60 - self.account.time_mgr.GetDatetime().minute) > 30:
            remainder -= 30
        return remainder * 60

    @property
    def next_hour(self) -> int:
        """下一个整小时"""
        return (60 - self.account.time_mgr.GetDatetime().minute) * 60

    @property
    def next_day(self) -> int:
        """第二天跳点"""
        now_time = self.account.time_mgr.GetDatetime()
        if now_time < 8:
            next_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 8, 0, 0, now_time.microsecond, tzinfo=now_time.tzinfo)
        else:
            next_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 8, 0, 0, now_time.microsecond, tzinfo=now_time.tzinfo) + datetime.timedelta(days=1)
        return (next_time - now_time).seconds

    @property
    def next_dinner(self) -> int:
        """下一次宴会"""
        now_time = self.account.time_mgr.GetDatetime()
        if now_time.hour < 10:
            dinner_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 10, 0, 0, now_time.microsecond, tzinfo=now_time.tzinfo)
        elif now_time.hour < 19:
            dinner_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 19, 0, 0, now_time.microsecond, tzinfo=now_time.tzinfo)
        else:
            dinner_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 10, 0, 0, now_time.microsecond, tzinfo=now_time.tzinfo) + datetime.timedelta(days=1)
        return (dinner_time - now_time).seconds
