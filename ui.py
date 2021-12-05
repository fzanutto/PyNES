import random
from cpu import CPU
import pygame
import sys

size = width, height = 960, 960


class UI():
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
        self.memory_owner = cpu.get_memory(0x200)

    def update_ui(self):
        self.cpu.set_memory(0xFE, random.randint(1, 16))
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
        # self.handle_user_input()
        # self.update_ui()
        pass
