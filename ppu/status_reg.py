from collections import OrderedDict
from enum import Enum

class PPUStatusReg:
    """
    7  bit  0
    ---- ----
    VSO. ....
    |||| ||||
    |||+-++++- Least significant bits previously written into a PPU register
    |||        (due to register not being updated for this address)
    ||+------- Sprite overflow. The intent was for this flag to be set
    ||         whenever more than eight sprites appear on a scanline, but a
    ||         hardware bug causes the actual behavior to be more complicated
    ||         and generate false positives as well as false negatives; see
    ||         PPU sprite evaluation. This flag is set during sprite
    ||         evaluation and cleared at dot 1 (the second dot) of the
    ||         pre-render line.
    |+-------- Sprite 0 Hit.  Set when a nonzero pixel of sprite 0 overlaps
    |          a nonzero background pixel; cleared at dot 1 of the pre-render
    |          line.  Used for raster timing.
    +--------- Vertical blank has started (0: not in vblank; 1: in vblank).
                Set at dot 1 of line 241 (the line *after* the post-render
                line); cleared after reading $2002 and at dot 1 of the
                pre-render line.
    """

    class StatusTypes(Enum):
        unused0 = 0  # 
        unused1 = 1  # 
        unused2 = 2  # 
        unused3 = 3  # 
        unused4 = 4 #
        overflow = 5 # O
        sprite_0_hit = 6  # S
        vblank = 7  # V

    def __init__(self):
        self.bits = OrderedDict([
            (PPUStatusReg.StatusTypes.unused0, False),
            (PPUStatusReg.StatusTypes.unused1, False),
            (PPUStatusReg.StatusTypes.unused2, True),
            (PPUStatusReg.StatusTypes.unused3, False),
            (PPUStatusReg.StatusTypes.unused4, False),
            (PPUStatusReg.StatusTypes.overflow, True),
            (PPUStatusReg.StatusTypes.sprite_0_hit, False),
            (PPUStatusReg.StatusTypes.vblank, True)
        ])

    def to_int(self) -> int:
        value = 0
        for i, bit in enumerate(self.bits.values()):
            value += int(bit) << i
        return value

    def from_int(self, value: int):
        for i in self.bits:
            self.bits[i] = (value & (1 << i.value)) > 0
