def GetSecondString(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60
    if minutes > 0:
        return f"{minutes}分钟{seconds}秒"
    return f"{seconds}秒"
