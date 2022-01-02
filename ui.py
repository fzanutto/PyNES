import random
from cpu import CPU
import pygame
import sys

from frame import Frame
from ppu.ppu import PPU

size = width, height = 256 * 4, 240 * 4


class UI:
    def __init__(self, cpu: CPU, chr_rom) -> None:
        self.cpu = cpu
        self.chr_rom = chr_rom
        self.frame = self.create_frame(chr_rom, 0)
        self.screen = pygame.display.set_mode(size)
        self.square = pygame.Surface((4,4))
        self.handle_and_update_ui = self.handle_ui
        self.memory_owner = self.cpu.bus.get_memory_owner(0x200)

    def update_ui(self):
        for x in range(Frame.WIDTH):
            for y in range(Frame.HEIGHT):
                color = self.frame.data[y * Frame.WIDTH + x]
                self.square.fill(color)
                draw = pygame.Rect((x*4)+1, (y*4)+1, 4, 4)
                self.screen.blit(self.square, draw)
        
        pygame.display.flip()

    def create_frame(self, chr_rom, bank: int) -> Frame:
        frame = Frame()

        bank = bank * 0x1000

        for tile_n in range(256):
            start_position = bank + tile_n * 16
            tile = chr_rom[start_position : start_position + 16]

            for y in range(8):
                upper = tile[y]
                lower = tile[y + 8]
                for x in range(7,-1,-1):
                    value = (1 & upper) << 1 | (1 & lower)
                    upper  = upper >> 1
                    lower = lower >> 1
                    
                    rgb = (0,0,0)
                    if value == 0:
                        rgb = PPU.SYSTEM_PALLETE[0x01]
                    elif value == 1:
                        rgb = PPU.SYSTEM_PALLETE[0x23]
                    elif value == 2:
                        rgb = PPU.SYSTEM_PALLETE[0x27]
                    elif value == 3:
                        rgb = PPU.SYSTEM_PALLETE[0x30]

                    true_x = x + ((tile_n % 20) * 8) + 1
                    true_y = y + ((tile_n // 20) * 8) + 1

                    frame.set_pixel(true_x, true_y, rgb)

        return frame

    def handle_user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 119:
                    # w
                    pass
                elif event.key == 97:
                    # a
                    pass
                elif event.key == 115:
                    # s
                    pass
                elif event.key == 100:
                    # d
                    pass

            if event.type == pygame.QUIT:
                sys.exit()

    def handle_ui(self):
        self.handle_user_input()
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
