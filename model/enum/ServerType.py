from enum import IntEnum, unique


@unique
class ServerType(IntEnum):
    """登录服务器类型"""
    YaoWan = 1  # 要玩
    PeiYou = 2  # 陪游


class ServerTypeString:
    type2name = {
        ServerType.YaoWan: "要玩",
        ServerType.PeiYou: "陪游",
    }

    @staticmethod
    def ToString(server_type: ServerType) -> str:
        return ServerTypeString.type2name.get(server_type, str(server_type))
