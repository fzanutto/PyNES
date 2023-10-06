import pygame
from time import time_ns
import sys
from frame import Frame
from io_registers import IO_Registers
from joypad import Joypad
from ppu.ppu import PPU
from cpu import CPU

PIXEL_SCALE = 4
size = width, height = 256, 240
from numpy.random import random, randint

class UI:
    def __init__(self, ppu: PPU, io_regs: IO_Registers, cpu: CPU):
        self.io_regs = io_regs
        self.ppu = ppu
        self.cpu = cpu
        self.frame = Frame()
        self.last_frame = Frame()
        self.screen = pygame.display.set_mode(size)
        self.square = pygame.Surface((PIXEL_SCALE, PIXEL_SCALE))
        self.update_ui_callback = self.update_ui
        self.last_frame_time = time_ns()

        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

    def update_ui(self):
        ppu_time = time_ns()
        self.ppu.render(self.frame)
        print("PPU:", (time_ns() - ppu_time) / 10**9)

        screen_time = time_ns()
        pixels = pygame.surfarray.pixels3d(self.screen)
        pixels[:, :, :] = self.frame.data

        # for x in range(Frame.WIDTH):
        #     for y in range(Frame.HEIGHT):
        #         new_color = self.frame.data[x][y]
        #         old_color = self.last_frame.data[x][y]
        #
        #         if new_color != old_color:
        #             pixels[x, y] = new_color
        del pixels

        pygame.display.flip()

        current_time = time_ns()
        diff = current_time - self.last_frame_time
        self.last_frame_time = current_time
        print("update screen time: {}".format((current_time - screen_time) / 10**9))
        print("FPS: {}. Time since last frame: {}".format(10**9 / diff, diff / 10**9))

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
                self.cpu.running = False
                sys.exit()
        