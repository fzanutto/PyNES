from io_registers import IO_Registers
from memory_owner import MemoryOwner
from ppu.ppu import PPU
from ram import RAM
from rom import ROM
import pygame
import sys

class Bus:
    def __init__(self, ram: RAM, ppu: PPU, io_regs: IO_Registers, rom: ROM):
        self.ram = ram
        self.ppu = ppu
        self.io_regs = io_regs
        self.rom = rom
        self.cycles = 0
        self.callback = None

        self.memory_owners: list[MemoryOwner] = [
            self.ram,
            self.ppu,
            self.io_regs,
            self.rom
        ]

    def get_actual_location(self, mem_owner: MemoryOwner, location: int) -> int:
        if type(mem_owner) is RAM:
            location &= ((1 << 11) - 1)

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

        current_nmi_state = self.ppu.nmi_interrupt
        self.ppu.tick(cycles * 3)
        new_nmi_state = self.ppu.nmi_interrupt

        if not current_nmi_state and new_nmi_state:
            self.callback()

        self.handle_joystick_input()

    def get_nmi_status(self):
        return self.ppu.get_and_update_nmi()
    
    def handle_joystick_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 119:
                    print("press w")
                    self.io_regs.joypad1.button_status = self.io_regs.joypad1.button_status | (1 << self.io_regs.joypad1.JoypadButton.UP)
                elif event.key == 97:
                    print("press a")
                    self.io_regs.joypad1.button_status = self.io_regs.joypad1.button_status | (1 << self.io_regs.joypad1.JoypadButton.LEFT)
                elif event.key == 115:
                    print("press s")
                    self.io_regs.joypad1.button_status = self.io_regs.joypad1.button_status | (1 << self.io_regs.joypad1.JoypadButton.DOWN)
                elif event.key == 100:
                    print("press d")
                    self.io_regs.joypad1.button_status = self.io_regs.joypad1.button_status | (1 << self.io_regs.joypad1.JoypadButton.RIGHT)

            if event.type == pygame.QUIT:
                sys.exit()