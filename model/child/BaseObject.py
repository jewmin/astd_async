ModelType = {}


def wrapper(cls):
    ModelType[cls.__name__.lower()] = cls
    return cls


class BaseObjectDict(dict):
    """对象基类字典"""

    def HandleXml(self, class_name: str, lst: list) -> None:
        clazz = ModelType[class_name]
        if not isinstance(lst, list):
            lst = [lst]
        for v in lst:
            o = clazz()
            o.HandleXml(v)
            kv = getattr(o, clazz.KEY)
            while isinstance(kv, BaseObject):
                kv = getattr(kv, kv.__class__.KEY)
            self[kv] = o


class BaseObjectList(list):
    """对象基类列表"""

    def HandleXml(self, class_name: str, lst: list) -> None:
        clazz = ModelType[class_name]
        if not isinstance(lst, list):
            lst = [lst]
        for v in lst:
            o = clazz()
            o.HandleXml(v)
            self.append(o)


class BaseObject:
    """对象基类"""

    def HandleXml(self, info: dict) -> None:
        if not info:
            return
        for k, v in info.items():
            if not hasattr(self, k):
                continue
            o = getattr(self, k)
            if isinstance(o, BaseObject):
                o.HandleXml(v)
            elif isinstance(o, (BaseObjectList, BaseObjectDict)):
                o.HandleXml(k, v)
            elif isinstance(o, bool):
                setattr(self, k, v == "1")
            elif isinstance(o, (int, float)):
                setattr(self, k, eval(v))
            else:
                setattr(self, k, v)
