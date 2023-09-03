from collections import OrderedDict
from enum import Enum

class PPUControlReg:
    """
    7  bit  0
    ---- ----
    VPHB SINN
    |||| ||||
    |||| ||++- Base nametable address
    |||| ||    (0 = $2000; 1 = $2400; 2 = $2800; 3 = $2C00)
    |||| |+--- VRAM address increment per CPU read/write of PPUDATA
    |||| |     (0: add 1, going across; 1: add 32, going down)
    |||| +---- Sprite pattern table address for 8x8 sprites
    ||||       (0: $0000; 1: $1000; ignored in 8x16 mode)
    |||+------ Background pattern table address (0: $0000; 1: $1000)
    ||+------- Sprite size (0: 8x8 pixels; 1: 8x16 pixels)
    |+-------- PPU master/slave select
    |          (0: read backdrop from EXT pins; 1: output color on EXT pins)
    +--------- Generate an NMI at the start of the
                vertical blanking interval (0: off; 1: on)
    """

    class StatusTypes(Enum):
        nametable1 = 0 # N
        nametable2 = 1 # N
        ram_increment = 2 # I
        sprite_pattern_addr = 3  # S
        background_pattern_addr = 4 # B
        sprite_size = 5 # H
        master_slave = 6  # P
        vblank = 7  # V

    def __init__(self):
        self.bits = OrderedDict([
            (PPUControlReg.StatusTypes.nametable1, False),
            (PPUControlReg.StatusTypes.nametable2, False),
            (PPUControlReg.StatusTypes.ram_increment, False),
            (PPUControlReg.StatusTypes.sprite_pattern_addr, False),
            (PPUControlReg.StatusTypes.background_pattern_addr, False),
            (PPUControlReg.StatusTypes.sprite_size, False),
            (PPUControlReg.StatusTypes.master_slave, False),
            (PPUControlReg.StatusTypes.vblank, False),
        ])

    def to_int(self) -> int:
        value = 0
        for i, bit in enumerate(self.bits.values()):
            value += int(bit) << i
        return value

    def from_int(self, value: int):
        for i in self.bits:
            self.bits[i] = (value & (1 << i.value)) > 0
