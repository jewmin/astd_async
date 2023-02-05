NumberString = ("", "万", "亿")


def GetSecondString(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60
    if minutes > 0:
        return f"{minutes}分钟{seconds}秒"
    return f"{seconds}秒"


def GetShortReadable(value: int) -> str:
    value = int(value)
    result = []
    for number_string in NumberString:
        if value >= 10000:
            result.append(f"{value % 10000}{number_string}")
            value //= 10000
        else:
            result.append(f"{value}{number_string}")
            break

    result.reverse()
    return "".join(result)
