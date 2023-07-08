from logic.ActivityConfig import activity_config
from task.BaseTask import BaseTask


class ActivityTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "活动"
        self.type = "unknown"
        self.config = activity_config.get(self.__class__.__name__, {})

    def Enable(self) -> bool:
        return self.HasActivity() and self.config.get("enable", False)

    def HasActivity(self) -> bool:
        return getattr(self.account.user, self.type, False)

    def info(self, msg, *args, **kwargs):
        self.account.logger.info(msg, *args, **kwargs)

    def GetConfig(self, key: str, default_value=None):
        return self.config.get(key, default_value)

    def GetAvailableGold(self):
        return self.account.user.get_available("gold")

    def IsAvailableAndSubGold(self, value):
        return self.account.user.is_available_and_sub("gold", value)
