from model.child.BaseObject import wrapper, BaseObject


@wrapper
class Ticket(BaseObject):
    """点券兑换物"""
    KEY = "item"

    def __init__(self):
        super().__init__()
        self.id = 0
        self.tickets = 0
        self.selltype = -1
        self.item = TicketItem()


@wrapper
class TicketItem(BaseObject):
    KEY = "name"

    def __init__(self):
        super().__init__()
        self.name = ""
        self.num = 0
