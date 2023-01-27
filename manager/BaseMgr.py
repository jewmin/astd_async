class BaseMgr:
    """管理基类"""
    def __init__(self, time_mgr, service_factory, user, index):
        super(BaseMgr, self).__init__()
        self.m_objTimeMgr = time_mgr
        self.m_objServiceFactory = service_factory
        self.m_objUser = user
        self.logger = getLogger(index)

    def get_protocol_mgr(self):
        return self.m_objServiceFactory.get_protocol_mgr()

    def get_service_factory(self):
        return self.m_objServiceFactory

    def add_task_finish_num(self, task_type, num):
        task = self.m_objUser.m_dictTasks.get(task_type, None)
        if task is not None:
            task.finishnum += num

    @staticmethod
    def get_impose_select_le(effect1, effect2):
        for v in config["impose"]["impose_event"]:
            if effect1.find(v) >= 0:
                return 1
            elif effect2.find(v) >= 0:
                return 2

    @staticmethod
    def get_formation_by_name(formation):
        formation_tuple = ("不变阵", "鱼鳞阵", "长蛇阵", "锋矢阵", "偃月阵", "锥形阵", "八卦阵", "七星阵", "雁行阵")
        for idx, value in enumerate(formation_tuple):
            if formation == value:
                return idx
        return 0

    @staticmethod
    def get_formation_by_id(formation_id):
        formation_tuple = ("不变阵", "鱼鳞阵", "长蛇阵", "锋矢阵", "偃月阵", "锥形阵", "八卦阵", "七星阵", "雁行阵")
        return formation_tuple[formation_id]
