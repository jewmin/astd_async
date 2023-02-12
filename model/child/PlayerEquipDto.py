from model.child.BaseObject import wrapper, BaseObject


@wrapper
class PlayerEquipDto(BaseObject):
    """套装"""
    KEY = "composite"

    def __init__(self):
        super().__init__()
        self.composite = 0
        self.equipname = ""
        self.generalname = ""
        self.canupgrade = False
        self.xuli = 0
        self.maxxuli = 0
        self.molicost = 0
        self.canmoli = False
        self.attfull = 0
        self.deffull = 0
        self.powerstr = ""
        self.tickets = 0
        self.ticketsstatus = 0
        self.monkeylv = 0
        self.powertao = 0

    def __repr__(self) -> str:
        power = self.powerstr.split(";")
        return f"套装[id={self.composite} name={self.equipname} general={self.generalname} 强攻({power[0]}/{self.attfull}) 强防({power[1]}/{self.deffull})]"
