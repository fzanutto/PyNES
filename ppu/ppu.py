from frame import Frame
from memory_owner import MemoryOwner
from ppu.control_reg import PPUControlReg
from ppu.mask_reg import PPUMaskReg
from ppu.status_reg import PPUStatusReg


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
        self.palette_table = [0] * 32
        self.ram = [0] * 2048
        self.oam_data = [0] * 256

        self.addr_reg = [0, 0]  # high, low
        self.addr_reg_pointer = 0
        self.internal_data_buf = 0
        self.mirror_mode = screen_mirroring  # 0: horizontal - 1: vertical
        self.control_reg = PPUControlReg()
        self.status_reg = PPUStatusReg()
        self.mask_reg = PPUMaskReg()
        self.oam_address_reg = 0
        self.oam_data_reg = 0

        self.scroll_reg = [0, 0] # x, y
        self.scroll_reg_pointer = 0

        self.current_cycle = 0
        self.scanline = 0
        self.nmi_interrupt = False

    def get_and_update_nmi(self):
        cur_value = self.nmi_interrupt
        self.nmi_interrupt = False
        return cur_value

    def increment_ram_addr(self):
        inc = 32 if self.control_reg.bits[PPUControlReg.StatusTypes.ram_increment] else 1

        self.set_addr_reg(self.get_addr_reg() + inc)

    def set_addr_reg(self, value):
        self.addr_reg[0] = (value >> 8) & 0x3F
        self.addr_reg[1] = value & 0xFF

    def get_addr_reg(self):
        return self.addr_reg[0] << 8 | self.addr_reg[1]

    def mirror_ram_addr(self, addr: int) -> int:
        mirrored_ram = addr & 0b00101111_11111111 # mirror down 0x3000-0x3eff to 0x2000 - 0x2eff
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
    
    def write_to_data(self, value):
        addr = self.get_addr_reg()

        if addr <= 0x1fff:
            raise Exception("attempt to write to chr rom space", addr)
        elif addr <= 0x3eff:
            self.ram[self.mirror_ram_addr(addr)] = value
        elif addr in [0x3f10, 0x3f14, 0x3f18, 0x3f1c]:
            address_mirror = addr - 0x10
            self.palette_table[address_mirror - 0x3f00] = value
        elif addr <= 0x3fff:
            self.palette_table[(addr - 0x3f00) % 0x20] = value
        else:
            raise Exception("unexpected access to address {}".format(addr))
        
        self.increment_ram_addr()

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
            address_mirror = addr - 0x10
            result = self.palette_table[address_mirror - 0x3f00]
        elif addr <= 0x3FFF:
            result = self.palette_table[(addr - 0x3f00) % 0x20]

        return result

    def write_oam_data(self, value: int):
        self.oam_data_reg = value
        self.oam_data[self.oam_address_reg] = value
        self.oam_address_reg = (self.oam_address_reg + 1) & 0xFF

    def set(self, position: int, value: int, size: int = 1):
        if position == 0x2000:
            self.update_control_reg(value)
        elif position == 0x2001:
            self.update_mask_reg(value)
        elif position == 0x2003:
            self.oam_address_reg = value
        elif position == 0x2004:
            self.write_oam_data(value)
        elif position == 0x2005:
            self.scroll_reg[self.scroll_reg_pointer] = value
            self.scroll_reg_pointer ^= 1
        elif position == 0x2006:
            self.addr_reg[self.addr_reg_pointer] = value & 0xFF
            self.addr_reg_pointer ^= 1
        elif position == 0x2007:
            self.write_to_data(value)
        elif 0x2008 <= position:
            self.set(position & 0b0010000000000111, value, size)
        else:
            super().set(position, value, size)

    def get(self, position: int) -> int:
        if position in [0x2000, 0x2001, 0x2003, 0x2005, 0x2006, 0x4014]:
            raise Exception("Trying to read write-only PPU address:", hex(position))
        elif position == 0x2002:
            value = self.status_reg.to_int()
            self.status_reg.bits[PPUStatusReg.StatusTypes.vblank] = 0
            self.addr_reg_pointer = 0
            self.scroll_reg_pointer = 0
            return value
        elif position == 0x2004:
            return self.oam_data_reg
        elif position == 0x2007:
            return self.read_data()

        elif position >= 0x2008:
            return self.get(position & 0b00100000_00000111)

        return super().get(position)

    def update_control_reg(self, value: int):
        current_nmi_status = self.control_reg.bits[PPUControlReg.StatusTypes.vblank]
        self.control_reg.from_int(value)
        new_nmi_status = self.control_reg.bits[PPUControlReg.StatusTypes.vblank]
        if not current_nmi_status and new_nmi_status and self.status_reg.bits[PPUStatusReg.StatusTypes.vblank] == 1:
            self.nmi_interrupt = True

    def update_mask_reg(self, value: int):
        self.mask_reg.from_int(value)

    def tick(self, cycles: int):
        self.current_cycle += cycles

        if 257 <= self.current_cycle <= 320:
            self.oam_address_reg = 0

        if self.current_cycle >= 341:
            if self.is_sprite_0_hit():
                self.status_reg.bits[PPUStatusReg.StatusTypes.sprite_0_hit] = 1

            self.current_cycle %= 341
            self.scanline += 1
            
            if self.scanline == 241:
                self.status_reg.bits[PPUStatusReg.StatusTypes.vblank] = 1
                self.status_reg.bits[PPUStatusReg.StatusTypes.sprite_0_hit] = 0
                if self.control_reg.bits[PPUControlReg.StatusTypes.vblank]:
                    self.nmi_interrupt = True

            elif self.scanline >= 262:
                self.scanline = 0
                self.status_reg.bits[PPUStatusReg.StatusTypes.sprite_0_hit] = 0
                self.status_reg.bits[PPUStatusReg.StatusTypes.vblank] = 0
                self.nmi_interrupt = False

    def is_sprite_0_hit(self) -> bool:
        y = self.oam_data[0]
        x = self.oam_data[3]
        return y == self.scanline and x <= self.current_cycle and self.mask_reg.bits[PPUMaskReg.StatusTypes.show_sprites] and self.mask_reg.bits[PPUMaskReg.StatusTypes.show_background]
                
    def get_background_pallete(self, column: int, row: int, attribute_table: list[int]):
        # https://www.nesdev.org/wiki/PPU_attribute_tables

        table_index = row // 4 * 8 + column // 4
        
        # bug: attribute table on last index is probably not being updated correctly
        # print(attribute_table[-1])
        byte = attribute_table[table_index]

        tile_column = (column % 4) // 2
        tile_row = (row % 4) // 2

        pallete_index = 0
        if tile_column == 0 and tile_row == 0:
            pallete_index = byte & 0b11
        elif tile_column == 1 and tile_row == 0:
            pallete_index = (byte >> 2) & 0b11
        elif tile_column == 0 and tile_row == 1:
            pallete_index = (byte >> 4) & 0b11
        elif tile_column == 1 and tile_row == 1:
            pallete_index = (byte >> 6) & 0b11

        pallete_start = 1 + pallete_index * 4
        return [
            self.palette_table[0],
            self.palette_table[pallete_start],
            self.palette_table[pallete_start + 1],
            self.palette_table[pallete_start + 2]
        ]
    
    def get_sprite_pallete(self, palllete_index: int):
        pallete_start = 0x11 + palllete_index * 4

        return [
            self.palette_table[0],
            self.palette_table[pallete_start],
            self.palette_table[pallete_start + 1],
            self.palette_table[pallete_start + 2]
        ]

    def render(self, frame: Frame):
        if self.mask_reg.bits[PPUMaskReg.StatusTypes.show_background]:
            self.render_background(frame)
        
        if self.mask_reg.bits[PPUMaskReg.StatusTypes.show_sprites]:
            sprite_16_8 = self.control_reg.bits[PPUControlReg.StatusTypes.sprite_size]
            self.render_sprites(frame, sprite_16_8)

    def render_background(self, frame: Frame):
        nametable_address = self.control_reg.get_nametable_addr()
        scroll_x = self.scroll_reg[0]
        scroll_y = self.scroll_reg[1]

        vertical_mirror = self.mirror_mode == 1

        main_nametable = None
        second_nametable = None

        if vertical_mirror: # SMB is vertical mirror
            if nametable_address in [0x2000, 0x2800]:
                main_nametable = self.ram[0 : 0x400]
                second_nametable = self.ram[0x400 : 0x800]
            elif nametable_address in [0x2400, 0x2C00]:
                main_nametable = self.ram[0x400 : 0x800]
                second_nametable = self.ram[0 : 0x400]
        else:
            if nametable_address in [0x2000, 0x2400]:
                main_nametable = self.ram[0 : 0x400]
                second_nametable = self.ram[0x400 : 0x800]
            elif nametable_address in [0x2800, 0x2C00]:
                main_nametable = self.ram[0x400 : 0x800]
                second_nametable = self.ram[0 : 0x400]

        bank = self.control_reg.bits[PPUControlReg.StatusTypes.background_pattern_addr]

        self.render_nametable(frame, bank, main_nametable, [scroll_x, scroll_y, 256, 240], -scroll_x, -scroll_y)

        if scroll_x > 0:
            self.render_nametable(frame, bank, second_nametable, [0, 0, scroll_x, 240], 256-scroll_x, 0)
        elif scroll_y > 0:
            self.render_nametable(frame, bank, second_nametable, [0, 0, 256, scroll_y], 0, 240-scroll_y)

    def render_nametable(self, frame: Frame, bank: bool, nametable: list[int], rect: list[int], shift_x: int, shift_y: int):
        attribute_table = nametable[0x3c0:]

        bank_index = 0x1000 if bank else 0
        for i in range(30 * 32):
            tile_index = self.ram[i]
            
            tile_column = i % 32
            tile_row = i // 32

            start_position = bank_index + tile_index * 16
            tile = self.chr_rom[start_position: start_position + 16]

            pallete_indexes = self.get_background_pallete(tile_column, tile_row, attribute_table)

            for y in range(8):
                upper = tile[y]
                lower = tile[y + 8]

                for x in range(7, -1, -1):
                    value = ((1 & lower) << 1) | (1 & upper)
                    upper = upper >> 1
                    lower = lower >> 1

                    rgb = PPU.SYSTEM_PALLETE[pallete_indexes[value]]

                    pixel_x = tile_column * 8 + x
                    pixel_y = tile_row * 8 + y

                    if rect[0] <= pixel_x < rect[2] and rect[1] <= pixel_y < rect[3]:
                        frame.set_pixel(shift_x + pixel_x, shift_y + pixel_y, rgb)

    def render_sprites(self, frame: Frame, sprite16: bool):
        bank = self.control_reg.bits[PPUControlReg.StatusTypes.sprite_pattern_addr]
        for i in range(len(self.oam_data) - 4, -1, -4):
            tile_index = self.oam_data[i + 1]
            tile_x = self.oam_data[i + 3]
            tile_y = self.oam_data[i]

            flip_vertical = self.oam_data[i + 2] >> 7 & 1
            flip_horizontal = self.oam_data[i + 2] >> 6 & 1

            pallete_index = self.oam_data[i + 2] & 0b11
            sprite_pallete = self.get_sprite_pallete(pallete_index)

            start_position = (0x1000 if bank else 0) + tile_index * 16
            tile = self.chr_rom[start_position: start_position + 16]

            for y in range(8):
                upper = tile[y]
                lower = tile[y + 8]

                for x in range(7, -1, -1):
                    value = ((1 & lower) << 1) | (1 & upper)
                    upper = upper >> 1
                    lower = lower >> 1

                    rgb = (0, 0, 0)
                    if value == 0:
                        continue
                    elif value == 1:
                        rgb = PPU.SYSTEM_PALLETE[sprite_pallete[1]]
                    elif value == 2:
                        rgb = PPU.SYSTEM_PALLETE[sprite_pallete[2]]
                    elif value == 3:
                        rgb = PPU.SYSTEM_PALLETE[sprite_pallete[3]]

                    final_x = tile_x + x
                    final_y = tile_y + y
                    if flip_horizontal:
                        final_x = tile_x + 7 - x

                    if flip_vertical:
                        final_y = tile_y + 7 - y

                    frame.set_pixel(final_x, final_y, rgb)
