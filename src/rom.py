from memory_owner import MemoryOwner

KB_SIZE = 1024


class ROM(MemoryOwner):
    # rom memory is duplicated around 0xC000
    memory_start_location = 0x8000
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes):
        self.header_size = 0x10  # 16 bytes
        self.rom_bytes = rom_bytes

        self.num_prg_blocks = self.rom_bytes[4]
        self.num_chr_rom_blocks = self.rom_bytes[5]

        control_byte_1 = self.rom_bytes[6]
        self.screen_mirroring = control_byte_1 & 1
        self.battery_ram = control_byte_1 & 0b10
        self.contains_trainer = control_byte_1 & 0b100
        self.four_screen_layout = control_byte_1 & 0b1000

        control_byte_2 = self.rom_bytes[7]
        # bits 0 and 1 should be 0 for ines 1.0
        self.ines_version = control_byte_2 & 0b1100

        if self.ines_version != 0:
            raise Exception("iNES version not supported yet")

        # control byte 1 container 4 lower bits and control byte 2 contain 4 upper bits of mapper type
        self.rom_mapper_type = (control_byte_2 & 0b1111_0000) | (control_byte_1 >> 4)

        prg_start = self.header_size + (0 if not self.contains_trainer else 512)
        prg_end = prg_start + (16 * KB_SIZE * self.num_prg_blocks)

        self.prg_bytes = rom_bytes[prg_start: prg_end]
        self.chr_rom = rom_bytes[prg_end: prg_end + (8 * KB_SIZE * self.num_chr_rom_blocks)]

    def get_memory(self):
        return self.prg_bytes

    def get(self, position: int, size: int = 1):
        initial_position = position - self.memory_start_location

        if self.num_prg_blocks == 1:
            initial_position %= 0x4000

        return int.from_bytes(self.get_memory()[initial_position: initial_position + size], byteorder='little')

    def get_bytes(self, position: int, size: int = 1):
        initial_position = position - self.memory_start_location

        if self.num_prg_blocks == 1:
            initial_position %= 0x4000

        return bytes(self.get_memory()[initial_position: initial_position + size])

    def set(self, position: int, value: int, size):
        raise Exception("Can't set read only memory")
