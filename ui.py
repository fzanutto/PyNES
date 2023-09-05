import random
from cpu import CPU
import pygame
import sys
from time import time_ns

from frame import Frame
from ppu.ppu import PPU

size = width, height = 256 * 4, 240 * 4


class UI:
    def __init__(self, cpu: CPU, ppu: PPU):
        self.cpu = cpu
        self.ppu = ppu
        self.chr_rom = ppu.chr_rom
        self.frame = Frame()
        self.screen = pygame.display.set_mode(size)
        self.square = pygame.Surface((4,4))
        self.handle_and_update_ui = self.handle_ui
        self.memory_owner = self.cpu.bus.get_memory_owner(0x200)
        self.start_time = time_ns()
        self.frame_count = 0

    def update_ui(self):
        if self.frame_count % 20 == 0:
            self.ppu.render(self.frame)
            
            for x in range(Frame.WIDTH):
                for y in range(Frame.HEIGHT):
                    color = self.frame.data[y * Frame.WIDTH + x]
                    self.square.fill(color)
                    draw = pygame.Rect((x*4)+1, (y*4)+1, 4, 4)
                    self.screen.blit(self.square, draw)
            
            pygame.display.flip()

        cur_time = time_ns()
        diff = cur_time - self.start_time
        
        self.frame_count += 1
        print("FPS: {}".format(10**9 * self.frame_count / diff))

    def handle_ui(self):
        self.update_ui()

class UI_Debug:
    def __init__(self, cpu: CPU) -> None:
        self.cpu = cpu
        self.screen = pygame.display.set_mode(size)
        self.handle_and_update_ui = self.handle_ui
        self.color_map = {
            0: pygame.color.THECOLORS['black'],
            1: pygame.color.THECOLORS['white'],
            2: pygame.color.THECOLORS['grey'],
            3: pygame.color.THECOLORS['red'],
            4: pygame.color.THECOLORS['green'],
            5: pygame.color.THECOLORS['blue'],
            6: pygame.color.THECOLORS['magenta'],
            7: pygame.color.THECOLORS['yellow'],
            8: pygame.color.THECOLORS['cyan'],
            9: pygame.color.THECOLORS['grey'],
            10: pygame.color.THECOLORS['red'],
            11: pygame.color.THECOLORS['green'],
            12: pygame.color.THECOLORS['blue'],
            13: pygame.color.THECOLORS['magenta'],
            14: pygame.color.THECOLORS['yellow'],
            15: pygame.color.THECOLORS['cyan'],
        }
        self.screen_buffer = [0] * 32 * 32
        self.memory_owner = self.cpu.bus.get_memory_owner(0x200)

    def update_ui(self):
        self.cpu.bus.write_memory(0xFE, random.randint(1, 16))
        mem = self.memory_owner.get_memory()[0x200: 0x600]
        for i in range(0x0200, 0x0600):
            index = i - 0x0200
            color_index = mem[index]
            r, g, b, a = self.color_map.get(color_index, pygame.color.THECOLORS['cyan'])

            rgb = (r, g, b)
            if self.screen_buffer[index] != rgb:
                self.screen_buffer[index] = rgb
                x = index % 32
                y = index // 32
                rect = pygame.Rect(x*30, y*30, 30, 30)
                self.screen.fill((r, g, b), rect)
                pygame.display.update(rect)

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 119:
                    # w
                    self.memory_owner.set(0xff, 0x77)
                elif event.key == 97:
                    # a
                    self.memory_owner.set(0xff, 0x61)
                elif event.key == 115:
                    # s
                    self.memory_owner.set(0xff, 0x73)
                elif event.key == 100:
                    # d
                    self.memory_owner.set(0xff, 0x64)

            if event.type == pygame.QUIT:
                sys.exit()

    def handle_ui(self):
        self.handle_user_input()
        self.update_ui()
