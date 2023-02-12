from model.child.BaseObject import wrapper, BaseObject


@wrapper
class EquipDto(BaseObject):
    """专属"""
    def __init__(self):
        super().__init__()
        self.storeid = 0
        self.quality = 0
        self.equipname = ""
        self.equiplevel = 0

    def __repr__(self) -> str:
        return f"专属[id={self.storeid} name={self.equipname} quality={self.quality} lv={self.equiplevel}]"
