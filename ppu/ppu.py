from frame import Frame
from memory_owner import MemoryOwner
from ppu.control_reg import ControlReg
from ppu.status_reg import StatusReg


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

    SYSTEM_PALLETE = [
        (0x80, 0x80, 0x80), (0x00, 0x3D, 0xA6), (0x00, 0x12, 0xB0), (0x44, 0x00, 0x96), (0xA1, 0x00, 0x5E),
        (0xC7, 0x00, 0x28), (0xBA, 0x06, 0x00), (0x8C, 0x17, 0x00), (0x5C, 0x2F, 0x00), (0x10, 0x45, 0x00),
        (0x05, 0x4A, 0x00), (0x00, 0x47, 0x2E), (0x00, 0x41, 0x66), (0x00, 0x00, 0x00), (0x05, 0x05, 0x05),
        (0x05, 0x05, 0x05), (0xC7, 0xC7, 0xC7), (0x00, 0x77, 0xFF), (0x21, 0x55, 0xFF), (0x82, 0x37, 0xFA),
        (0xEB, 0x2F, 0xB5), (0xFF, 0x29, 0x50), (0xFF, 0x22, 0x00), (0xD6, 0x32, 0x00), (0xC4, 0x62, 0x00),
        (0x35, 0x80, 0x00), (0x05, 0x8F, 0x00), (0x00, 0x8A, 0x55), (0x00, 0x99, 0xCC), (0x21, 0x21, 0x21),
        (0x09, 0x09, 0x09), (0x09, 0x09, 0x09), (0xFF, 0xFF, 0xFF), (0x0F, 0xD7, 0xFF), (0x69, 0xA2, 0xFF),
        (0xD4, 0x80, 0xFF), (0xFF, 0x45, 0xF3), (0xFF, 0x61, 0x8B), (0xFF, 0x88, 0x33), (0xFF, 0x9C, 0x12),
        (0xFA, 0xBC, 0x20), (0x9F, 0xE3, 0x0E), (0x2B, 0xF0, 0x35), (0x0C, 0xF0, 0xA4), (0x05, 0xFB, 0xFF),
        (0x5E, 0x5E, 0x5E), (0x0D, 0x0D, 0x0D), (0x0D, 0x0D, 0x0D), (0xFF, 0xFF, 0xFF), (0xA6, 0xFC, 0xFF),
        (0xB3, 0xEC, 0xFF), (0xDA, 0xAB, 0xEB), (0xFF, 0xA8, 0xF9), (0xFF, 0xAB, 0xB3), (0xFF, 0xD2, 0xB0),
        (0xFF, 0xEF, 0xA6), (0xFF, 0xF7, 0x9C), (0xD7, 0xE8, 0x95), (0xA6, 0xED, 0xAF), (0xA2, 0xF2, 0xDA),
        (0x99, 0xFF, 0xFC), (0xDD, 0xDD, 0xDD), (0x11, 0x11, 0x11), (0x11, 0x11, 0x11)
    ]

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
        self.control_reg = ControlReg()
        self.status_reg = StatusReg()

        self.scroll_reg = [0, 0] # high, low
        self.scroll_reg_pointer = 0

        self.cycles = 0
        self.scanline = 0
        self.nmi_interrupt = False

    def increment_ram_addr(self):
        inc = 32 if (self.control_reg.bits[ControlReg.StatusTypes.ram_increment]) > 0 else 1

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

    def get_scroll_reg(self, value):
        return (self.scroll_reg[0] << 8 | self.scroll_reg[1]) & int('0b11111111111111', 2)

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
        elif addr in [0x3f10, 0x3f14, 0x3f18, 0x3f1c]:
            add_mirror = addr - 0x10
            result = self.palette_table[add_mirror - 0x3f00]
        elif addr <= 0x3FFF:
            result = self.palette_table[addr - 0x3f00]

        return result

    def write_oam_data(self, value: int):
        if self.status_reg.bits[StatusReg.StatusTypes.vblank] == 1:
            self.get_memory()[0x2003 - self.memory_start_location] = (self.get_memory()[0x2003 - self.memory_start_location] + 1) & 255

        super().set(0x2004, value, 1)

    def set(self, position: int, value: int, size: int = 1):
        if position == 0x2000:
            self.update_control_reg(value)
        elif position == 0x2004:
            self.write_oam_data(value)
        elif position == 0x2005:
            self.scroll_reg[self.scroll_reg_pointer] = value
            self.scroll_reg_pointer ^= 1
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
        elif position == 0x2002:
            value = self.status_reg.to_int()
            self.status_reg.bits[StatusReg.StatusTypes.vblank] = 0
            self.addr_reg_pointer = 0
            self.scroll_reg_pointer = 0
            return value
        elif position == 0x2007:
            return self.read_data()

        elif position >= 0x2008:
            return self.get(position & int('0b00100000_00000111', 2))

        return super().get(position)

    def update_control_reg(self, value: int):
        current_nmi_status = self.control_reg.bits[ControlReg.StatusTypes.vblank]
        self.control_reg.from_int(value)
        new_nmi_status = self.control_reg.bits[ControlReg.StatusTypes.vblank]
        if not current_nmi_status and new_nmi_status and self.status_reg.bits[StatusReg.StatusTypes.vblank] == 1:
            self.nmi_interrupt = True

    def tick(self, cycles: int):
        self.cycles += cycles

        if self.cycles >= 341:
            self.cycles %= 341

            self.scanline += 1

            if self.scanline == 241:
                if self.control_reg.bits[ControlReg.StatusTypes.vblank]:
                    self.status_reg.bits[StatusReg.StatusTypes.vblank] = 1
                    self.nmi_interrupt = True

            elif self.scanline >= 262:
                self.scanline = 0
                self.status_reg.bits[StatusReg.StatusTypes.sprite_0_hit] = 0
                self.status_reg.bits[StatusReg.StatusTypes.vblank] = 0
                self.nmi_interrupt = False
                

    def render(self, frame: Frame):
        bank = self.control_reg.bits[ControlReg.StatusTypes.background_pattern_addr]
        frame = Frame()
        for i in 0x03C0:
            tile = self.ram[i]
            tile_x = i % 32
            tile_y = i // 32

            start_position = bank + tile * 16
            tile = self.chr_rom[start_position: start_position + 16]

            for y in range(8):
                upper = tile[y]
                lower = tile[y + 8]
                for x in range(8, -1, -1):
                    value = (1 & upper) | (1 & lower)
                    upper = upper >> 1
                    lower = lower >> 1

                    rgb = (0,0,0)
                    if value == 0:
                        rgb = PPU.SYSTEM_PALLETE[0x01]
                    elif value == 1:
                        rgb = PPU.SYSTEM_PALLETE[0x23]
                    elif value == 2:
                        rgb = PPU.SYSTEM_PALLETE[0x27]
                    elif value == 3:
                        rgb = PPU.SYSTEM_PALLETE[0x30]

                    frame.set_pixel(tile_x * 8 + x,tile_y * 8 + y, rgb)