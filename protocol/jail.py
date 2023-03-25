import manager.ProtocolMgr as ProtocolMgr
import logic.Format as Format

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("监狱", sub_module=False)
async def jail(account: 'Account', result: 'ServerResult'):
    if result.success:
        if "remaintime" not in result.result:
            per_gold = int(result.result["pergold"])
            if per_gold <= account.user.get_available("gold"):
                await techResearch(account)
        return result.result["jailwork"]
    return ()


async def doJail(account: 'Account', get_baoshi: bool):
    jail_works = await jail(account)
    for jail_work in jail_works:
        if jail_work["canget"] == "1":
            jail_id = int(jail_work["id"]) - 1
            if get_baoshi:
                await recvJailWork(account, type=0, weizhi=jail_id)
            else:
                await recvJailWork(account, type=1, weizhi=jail_id)


@ProtocolMgr.Protocol("技术研究")
async def techResearch(account: 'Account', result: 'ServerResult'):
    if result.success:
        remain_time = int(result.result["remaintime"])
        account.logger.info("监狱技术研究, 剩余时间: %s", account.time_mgr.GetDatetimeString(remain_time))


@ProtocolMgr.Protocol("监狱劳作", ("type", "weizhi"))
async def recvJailWork(account: 'Account', result: 'ServerResult', type, weizhi):
    if result.success:
        if "baoshi" in result.result:
            account.logger.info("监狱劳作, 获得宝石+%s", Format.GetShortReadable(result.result["baoshi"]))
        elif "bintie" in result.result:
            account.logger.info("监狱劳作, 获得镔铁+%s", Format.GetShortReadable(result.result["bintie"]))


@ProtocolMgr.Protocol("从监狱逃跑")
async def escape(account: 'Account', result: 'ServerResult'):
    if result.success:
        cd = int(result.result["cd"])
        account.logger.info("从监狱逃跑, 冷却时间：%d秒", cd)
        return cd
