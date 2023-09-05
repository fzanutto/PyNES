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
        self.callback = None

        self.memory_owners: list[MemoryOwner] = [
            self.ram,
            self.ppu,
            self.io_regs,
            self.rom
        ]

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
        return mem_owner.get(position)

    def read_memory_bytes(self, position: int, size: int = 1) -> bytes:
        mem_owner = self.get_memory_owner(position)
        value = mem_owner.get_bytes(position, size)

        if type(value) is list and len(value) > 0 and type(value[0]) is bytes:
            value = b''.join(value)

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

        if not current_nmi_state and new_nmi_state:
            self.callback()

        self.handle_joystick_input()

    def get_nmi_status(self):
        return self.ppu.get_and_update_nmi()
    
    def handle_joystick_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.UP
                elif event.key == pygame.K_LEFT:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.LEFT
                elif event.key == pygame.K_DOWN:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.DOWN
                elif event.key == pygame.K_RIGHT:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.RIGHT
                elif event.key == pygame.K_z:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.BUTTON_A
                elif event.key == pygame.K_x:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.BUTTON_B
                elif event.key == pygame.K_a:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.START
                elif event.key == pygame.K_s:
                    self.io_regs.joypad1.button_status |= Joypad.JoypadButton.SELECT

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.UP
                elif event.key == pygame.K_LEFT:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.LEFT
                elif event.key == pygame.K_DOWN:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.DOWN
                elif event.key == pygame.K_RIGHT:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.RIGHT
                elif event.key == pygame.K_z:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.BUTTON_A
                elif event.key == pygame.K_x:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.BUTTON_B
                elif event.key == pygame.K_a:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.START
                elif event.key == pygame.K_s:
                    self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.SELECT

            elif event.type == pygame.QUIT:
                sys.exit()