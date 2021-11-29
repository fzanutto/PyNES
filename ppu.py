from memory_owner import MemoryOwnerMixin


class PPU(MemoryOwnerMixin, object):
    '''
    $2000 -> PPUCTRL: PPU control register. Access: write
    $2001 -> PPUMASK: PPu mask register. Access: write
    $2002 -> PPUSTATUS: PPU status register. Access: read
    $2003 -> OAMADDR: OAM address port. Access: write
    $2004 -> OAMDATA: OAM data port. Access: read, write
    $2005 -> PPUSCROLL: PPU scrolling position register. Access: write twice
    $2006 -> PPUADDR: PPU address register. Access: write twice
    $2007 -> PPUDATA: PPU data register. Access: read, write
    '''
    memory_start_location = 0x2000
    memory_end_location = 0x2007

    def __init__(self):
        self.memory: list[int] = [0]*8

    def get_memory(self) -> list[int]:
        return self.memory
