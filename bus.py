from io_registers import IO_Registers
from memory_owner import MemoryOwner
from ppu.ppu import PPU
from ram import RAM
from rom import ROM


class Bus:
    def __init__(self, ram: RAM, ppu: PPU, io_regs: IO_Registers, rom: ROM):
        self.ram = ram
        self.ppu = ppu
        self.io_regs = io_regs
        self.rom = rom
        self.cycles = 0

        self.memory_owners: list[MemoryOwner] = [
            self.ram,
            self.ppu,
            self.io_regs,
            self.rom
        ]

    def get_actual_location(self, mem_owner: MemoryOwner, location: int) -> int:
        if type(mem_owner) is RAM:
            location &= ((1 << 11) - 1)

        elif type(mem_owner) is ROM:
            while location >= 0xC000:
                location -= 0x4000

        return location

    def get_memory_owner(self, location: int):
        """
        return the owner of a memory location
        """
        # check if memory owner
        for memory_owner in self.memory_owners:
            if memory_owner.memory_start_location <= location <= memory_owner.memory_end_location:
                return memory_owner

        raise Exception('Cannot find memory owner', location)

    def read_memory(self, position: int):
        mem_owner = self.get_memory_owner(position)

        actual_position = self.get_actual_location(mem_owner, position)
        return mem_owner.get(actual_position)

    def read_memory_bytes(self, position: int, size: int = 1) -> bytes:
        mem_owner = self.get_memory_owner(position)

        position = self.get_actual_location(mem_owner, position)

        value = mem_owner.get_bytes(position, size)

        if type(value) is list and len(value) > 0 and type(value[0]) is bytes:
            value = b''.join(value)

        return bytes(value)

    def write_memory(self, position: int, value: int, num_bytes: int = 1):
        mem_owner = self.get_memory_owner(position)

        position = self.get_actual_location(mem_owner, position)

        mem_owner.set(position, value, num_bytes)

    def tick(self, cycles: int):
        self.cycles += cycles
        self.ppu.tick(cycles * 3)

    def get_nmi_status(self):
        return self.ppu.get_and_update_nmi()