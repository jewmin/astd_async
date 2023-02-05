from model.child.BaseObject import wrapper, BaseObject
import logic.Format as Format


@wrapper
class SupperMarketDto(BaseObject):
    """集市商品"""
    def __init__(self, info: dict = None):
        super().__init__()
        self.id = 0
        self.price = ""
        self.name = ""
        self.num = 0
        self.baoshinum = 0
        self.finalprice = 0
        self.quality = 0
        self.HandleXml(info)

    def get_price(self):
        price_type, _ = self.price.split(":")
        return price_type, int(self.finalprice)

    def __repr__(self) -> str:
        num = Format.GetShortReadable(self.baoshinum) if self.baoshinum > 0 else Format.GetShortReadable(self.num)
        price_type, price = self.get_price()
        cost = "银币" if price_type == "copper" else "金币"
        return f"[{self.name}+{num}]({cost}-{Format.GetShortReadable(price)})"


@wrapper
class SupperMarketSpecialDto(BaseObject):
    """集市特殊商品"""
    def __init__(self):
        super().__init__()
        self.id = 0
        self.price = ""
        self.itemname = "宝石"
        self.num = 0
        self.state = 0

    def get_price(self):
        price_type, price = self.price.split(":")
        return price_type, int(price)

    def __repr__(self) -> str:
        num = Format.GetShortReadable(self.num)
        price_type, price = self.get_price()
        cost = "银币" if price_type == "copper" else "金币"
        return f"[{self.itemname}+{num}]({cost}-{Format.GetShortReadable(price)})"
