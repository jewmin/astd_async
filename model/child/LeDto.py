from model.child.BaseObject import wrapper, BaseObject

# flake8: noqa

RewardMaps = {
    "l": "民忠",
    "f": "威望",
    "s": "银币",
    "g": "金币",
    "t": "征收次数",
    "c": "征收CD",
}


@wrapper
class LeDto(BaseObject):
    """征收问题"""
    def __init__(self):
        super().__init__()
        self.l = 0
        self.f = 0
        self.s = 0
        self.g = 0
        self.t = 0
        self.c = 0

    def __repr__(self) -> str:
        strings = []
        for k, kk in RewardMaps.items():
            v = getattr(self, k)
            if v > 0:
                strings.append(f"{kk}+{v}")
            elif v < 0:
                strings.append(f"{kk}{v}")
        return ", ".join(strings)
