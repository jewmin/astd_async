import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403
import logic.Format as Format

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("点券商城", sub_module=False)
async def tickets(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        account.user.tickets = int(result.result["tickets"])
        account.user.ticket_exchange.HandleXml('Ticket', result.result["rewards"]["reward"])


@ProtocolMgr.Protocol("兑换奖励", ("rewardId", "num"))
async def getTicketsReward(account: 'Account', result: 'ServerResult', kwargs: dict):
    if result.success:
        ticket: Ticket = kwargs["ticket"]  # noqa: F405
        use_tickets = Format.GetShortReadable(ticket.tickets * kwargs["num"])
        get_num = Format.GetShortReadable(ticket.item.num * kwargs["num"])
        account.logger.info("兑换奖励, 花费%s点券, 获得%s+%s", use_tickets, ticket.item.name, get_num)


async def doGetTicketsReward(account: 'Account', name: str, num: int):
    if (ticket := account.user.ticket_exchange.get(name)) is not None:
        await getTicketsReward(account, rewardId=ticket.id, num=num, ticket=ticket)
