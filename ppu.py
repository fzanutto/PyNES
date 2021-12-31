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

    NAMETABLE1 = int('0b00000001', 2)
    NAMETABLE2 = int('0b00000010', 2)
    VRAM_ADD_INCREMENT = int('0b00000100', 2)
    SPRITE_PATTERN_ADDR = int('0b00001000', 2)
    BACKROUND_PATTERN_ADDR = int('0b00010000', 2)
    SPRITE_SIZE = int('0b00100000', 2)
    MASTER_SLAVE_SELECT = int('0b01000000', 2)
    GENERATE_NMI = int('0b10000000', 2)

    def __init__(self, chr_rom: bytes, screen_mirroring: int):
        super().__init__(0x2000, 0x3FFF)

        self.chr_rom = chr_rom
        self.palette_table = [0 * 32]
        self.ram = [0 * 2048]
        self.oam_data = [0 * 256]

        self.addr_reg = [0, 0]  # high, low
        self.addr_reg_pointer = 0
        self.internal_data_buf = 0
        self.mirror_mode = screen_mirroring  # 0: horizontal - 1: vertical

    def set_control_reg(self, value):
        self.memory[0] = value

    def get_control_reg(self):
        return self.memory[0]

    def increment_ram_addr(self):
        inc = 32 if (self.get_control_reg() & self.VRAM_ADD_INCREMENT) > 0 else 1

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
        return (self.addr_reg[0] << 8 | self.addr_reg[1]) & int('0b11111111111111', 2)


    def write_to_data(self, value):
        addr = self.get_addr_reg()

        if addr <= 0x1fff:
            raise Exception("attempt to write to chr rom space", addr)
        elif addr <= 0x2fff:
            self.ram[self.mirror_ram_addr(addr)] = value
        elif addr <= 0x3eff:
            raise Exception("addr {} shouldn't be used in reallity".format(addr))
        elif addr in [0x3f10, 0x3f14, 0x3f18, 0x3f1c]:
            add_mirror = addr - 0x10
            self.palette_table[add_mirror - 0x3f00] = value
        else:
            raise Exception("unexpected access to mirrored space {}".format(addr))
        
        self.increment_ram_addr()

    def mirror_ram_addr(self, addr: int) -> int:
        mirrored_ram = addr & int('0b10111111111111', 2)
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
            result = self.palette_table[addr - 0x3f00]

        return result

    def set(self, position: int, value: int, size: int = 1):
        if position == 0x2000:
            self.set_control_reg(value)
        elif position == 0x2006:
            self.addr_reg[self.addr_reg_pointer] = value
            self.addr_reg_pointer ^= 1
        elif position == 0x2007:
            self.write_to_data(value)
        elif 0x2008 <= position:
            self.set(position & int('0b0010000000000111', 2), value, size)
        else:
            super().set(position, value, size)

    def get(self, position: int) -> int:
        if position in [0x2000, 0x2001, 0x2003, 0x2005, 0x2006, 0x4014]:
            raise Exception("Trying to read write-only PPU address:", hex(position))

        elif position == 0x2007:
            return self.read_data()

        elif position >= 0x2008:
            return self.get(position & int('0b00100000_00000111', 2))

        return super().get(position)
