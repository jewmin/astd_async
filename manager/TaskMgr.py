from weakref import proxy
from task.BaseTask import BaseTask


class TaskMgr:
    """任务管理"""
    def __init__(self):
        self.tasks: dict[str, BaseTask] = {}

    def AddTask(self, task: BaseTask):
        assert task.name not in self.tasks
        task.task_mgr = proxy(self)
        self.tasks[task.name] = task

    def RunAllTasks(self):
        for task in self.tasks.values():
            task.Run()

    def RunTask(self, name: str):
        if (task := self.tasks.get(name)) is not None:
            task.Cancel()
            task.Run()

    def StopAllTasks(self):
        for task in self.tasks.values():
            task.Cancel()
