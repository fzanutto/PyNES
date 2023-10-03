from collections import OrderedDict
from enum import Enum


class PPUMaskReg:
    """
    7  bit  0
    ---- ----
    BGRs bMmG
    |||| ||||
    |||| |||+- Greyscale (0: normal color, 1: produce a greyscale display)
    |||| ||+-- 1: Show background in leftmost 8 pixels of screen, 0: Hide
    |||| |+--- 1: Show sprites in leftmost 8 pixels of screen, 0: Hide
    |||| +---- 1: Show background
    |||+------ 1: Show sprites
    ||+------- Emphasize red (green on PAL/Dendy)
    |+-------- Emphasize green (red on PAL/Dendy)
    +--------- Emphasize blue
    """

    class StatusTypes(Enum):
        greyscale = 0 # G
        background_left = 1 # m
        sprites_left = 2 # M
        show_background = 3  # b
        show_sprites = 4 # s
        emphasize_red = 5 # R
        emphasize_green = 6  # G
        emphasize_blue = 7  # B

    def __init__(self):
        self.bits = OrderedDict([
            (PPUMaskReg.StatusTypes.greyscale, False),
            (PPUMaskReg.StatusTypes.background_left, False),
            (PPUMaskReg.StatusTypes.sprites_left, False),
            (PPUMaskReg.StatusTypes.show_background, False),
            (PPUMaskReg.StatusTypes.show_sprites, False),
            (PPUMaskReg.StatusTypes.emphasize_red, False),
            (PPUMaskReg.StatusTypes.emphasize_green, False),
            (PPUMaskReg.StatusTypes.emphasize_blue, False)
        ])

    def to_int(self) -> int:
        value = 0
        for i, bit in enumerate(self.bits.values()):
            value += int(bit) << i
        return value

    def from_int(self, value: int):
        for i in self.bits:
            self.bits[i] = (value & (1 << i.value)) > 0
