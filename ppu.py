from memory_owner import MemoryOwner


class PPU(MemoryOwner):
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

    NAMETABLE1 = '0b00000001'
    NAMETABLE2 = '0b00000010'
    VRAM_ADD_INCREMENT = '0b00000100'
    SPRITE_PATTERN_ADDR = '0b00001000'
    BACKROUND_PATTERN_ADDR = '0b00010000'
    SPRITE_SIZE = '0b00100000'
    MASTER_SLAVE_SELECT = '0b01000000'
    GENERATE_NMI = '0b10000000'

    def __init__(self):
        super().__init__(0x2000, 0x3FFF)

        self.addr_reg = [0, 0]  # high, low
        self.addr_reg_pointer = 0
        self.internal_data_buf = 0
        self.chr_rom = []
        self.mirror_mode = None  # 0: horizontal - 1: vertical

    def set_chr_rom(self, data):
        self.chr_rom = data

    def set_screen_mirroring(self, data):
        self.mirror_mode = data

    def set_control_reg(self, value):
        self.memory[0] = value

    def get_control_reg(self):
        return self.memory[0]

    def increment_ram_addr(self):
        inc = 32 if self.get_control_reg() & self.VRAM_ADD_INCREMENT > 0 else 1

        low_addr = self.addr_reg[1]
        self.addr_reg[1] = (self.addr_reg[1] + inc) & 0xFF

        if low_addr > self.addr_reg[1]:
            self.addr_reg[0] = (self.addr_reg[0] + inc) & 0xFF

        addr = self.get_addr_reg()
        if addr > 0x3FFF:
            self.set_addr_reg(addr & 0x3FFF)

    def set_addr_reg(self, value):
        self.addr_reg[0] = value >> 8
        self.addr_reg[1] = value & 0xFF

    def get_addr_reg(self):
        return self.addr_reg[0] << 8 | self.addr_reg[1]

    def mirror_ram_addr(self, addr):
        mirrored_ram = addr & '0b10111111111111'
        ram_index = mirrored_ram - 0x2000
        name_table = ram_index // 0x400
        if self.mirror_mode == 0:  # horizontal
            if name_table == 1 or name_table == 2:
                return ram_index - 0x400
            elif name_table == 3:
                return ram_index - 0x800
        elif self.mirror_mode == 1:  # vertical
            if name_table == 2 or name_table == 3:
                return ram_index - 0x800

        return ram_index

    def read_data(self):
        addr = self.get_addr_reg()

        self.increment_ram_addr()

        result = self.internal_data_buf
        if addr <= 0x1FFF:
            self.internal_data_buf = self.chr_rom[addr]
        elif addr <= 0x2FFF:
            self.internal_data_buf = self.ram[self.mirror_ram_addr(addr)]
        elif addr <= 0x3EFF:
            raise Exception("Addr not expected to be used")
        elif addr <= 0x3FFF:
            result = self.pallete_table[addr - 0x3f00]

        return result

    def set(self, position: int, value: int, size: int = 1):

        if position == 0x2000:
            self.set_control_reg(value)
        elif position == 0x2007:
            self.addr_reg[self.addr_reg_pointer] = value
            self.addr_reg_pointer ^= 1

        super().set(position, value, size)

    def get(self, position: int) -> int:
        if position in [0x2000, 0x2001, 0x2003, 0x2005, 0x2006, 0x4014]:
            raise Exception("Trying to read write-only PPU address:", hex(position))

        elif position == 0x2007:
            return self.read_data()

        elif position >= 0x2008:
            return self.get(position & '0b00100000_00000111')

        return super().get(position)
