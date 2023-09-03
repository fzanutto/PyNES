from typing import List

from memory_owner import MemoryOwner

KB_SIZE = 1024


class ROM(MemoryOwner):
    # rom memory is duplicated around 0xC000
    memory_start_location = 0x8000
    memory_end_location = 0xFFFF

    def __init__(self, rom_bytes: bytes, is_test_rom: bool = False):
        self.is_snake_rom = is_test_rom

        if not self.is_snake_rom:
            self.header_size = 0x10  # 16 bytes
            self.rom_bytes = rom_bytes

            self.num_prg_blocks = self.rom_bytes[4]
            self.num_chr_rom_blocks = self.rom_bytes[5]
            # TODO flags 6, 7, 8, 9, 10

            self.flag_6 = self.rom_bytes[6]

            prg_start = self.header_size
            prg_end = self.header_size + (16 * KB_SIZE * self.num_prg_blocks)
            # program data starts after header
            # and lasts for a set number of 16KB blocks
            self.prg_bytes = rom_bytes[prg_start: prg_end]
            self.chr_rom = rom_bytes[prg_end: prg_end + (8 * KB_SIZE * self.num_chr_rom_blocks)]
        else:
            self.header_size = 0
            self.rom_bytes = rom_bytes
            self.prg_bytes = rom_bytes
            self.num_prg_blocks = 1
            self.num_chr_rom_blocks = 1

    def get_memory(self) -> List[bytes]:
        return self.prg_bytes

    def get(self, position: int, size: int = 1) -> bytes:
        initial_position = position - self.memory_start_location

        if self.num_prg_blocks == 1:
            initial_position %= 0x4000

        return self.get_memory()[initial_position: initial_position + size]

    def get_bytes(self, position: int, size: int = 1):
        initial_position = position - self.memory_start_location

        if self.num_prg_blocks == 1:
            initial_position %= 0x4000

        return bytes(self.get_memory()[initial_position: initial_position + size])

    def set(self, position: int, value: int):
        raise Exception("Can't set read only memory")
