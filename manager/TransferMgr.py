from aiohttp import ClientSession, ClientResponse
import engine.LogManager as LogManager

Logger = LogManager.GetLogger("TransferMgr")


async def Response(resp: ClientResponse) -> str:
    if resp is None or resp.status == 0:
        return "code:-1"
    elif resp.status != 200 and resp.status != 304:
        return f"code:{resp.status}"
    else:
        content = await resp.text()
        index = content.find("<results>")
        if index < 0:
            return ""
        else:
            return content[index:]


async def Get(url: str, cookies: dict) -> str:
    resp = await GetPure(url, cookies)
    return await Response(resp)


async def Post(url: str, data: dict, cookies: dict) -> str:
    resp = await PostPure(url, data, cookies)
    return await Response(resp)


async def GetPure(url: str, cookies: dict, headers: dict = None) -> ClientResponse:
    try:
        async with ClientSession(cookies=cookies, headers=headers) as session:
            async with session.get(url, allow_redirects=False) as resp:
                cookies.update(resp.cookies)
                return resp
    except Exception:
        Logger.LogLastExcept()


async def PostPure(url: str, data: dict, cookies: dict, headers: dict = None) -> ClientResponse:
    try:
        async with ClientSession(cookies=cookies, headers=headers, auto_decompress=True) as session:
            async with session.post(url, data=data, allow_redirects=False) as resp:
                cookies.update(resp.cookies)
                return resp
    except Exception:
        Logger.LogLastExcept()
