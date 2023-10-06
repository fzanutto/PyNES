from io_registers import IO_Registers
from memory_owner import MemoryOwner
from ppu.ppu import PPU
from ram import RAM
from rom import ROM
import pygame
import sys
from joypad import Joypad


class Bus:
    def __init__(self, ram: RAM, ppu: PPU, io_regs: IO_Registers, rom: ROM):
        self.ram = ram
        self.ppu = ppu
        self.io_regs = io_regs
        self.rom = rom
        self.update_ui_callback = None
        self.joystick_input_callback = None

        self.memory_owners: list[MemoryOwner] = [
            self.ram,
            self.ppu,
            self.io_regs,
            self.rom
        ]

    def get_memory_owner(self, location: int):
        if location <= 0x1FFF:
            return self.ram
        elif location <= 0x3FFF:
            return self.ppu
        elif location <= 0x401F:
            return self.io_regs
        else:
            return self.rom

    def read_memory(self, position: int):
        mem_owner = self.get_memory_owner(position)
        return mem_owner.get(position)

    def read_memory_bytes(self, position: int, size: int = 1) -> bytes:
        mem_owner = self.get_memory_owner(position)
        value = mem_owner.get_bytes(position, size)

        return bytes(value)

    def write_memory(self, position: int, value: int, num_bytes: int = 1):
        mem_owner = self.get_memory_owner(position)

        if position == 0x4014:
            self.write_to_oam_dma(value)

        mem_owner.set(position, value, num_bytes)

    def write_to_oam_dma(self, location: int):
        for i in range(0xFF):
            value = self.read_memory((location << 8) | i)
            self.ppu.write_oam_data(value)
        
    def tick(self, cycles: int):
        current_nmi_state = self.ppu.nmi_interrupt
        self.ppu.tick(cycles * 3)
        new_nmi_state = self.ppu.nmi_interrupt

        if not current_nmi_state and new_nmi_state and self.update_ui_callback is not None:
            self.joystick_input_callback()
            self.update_ui_callback()

    def get_nmi_status(self):
        return self.ppu.get_and_update_nmi()
