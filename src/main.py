from tkinter import *
from tkinter import filedialog
from bus import Bus
from cpu import CPU
from gameframe import GameFrame
from io_registers import IO_Registers
from ppu.ppu import PPU
from ram import RAM
from rom import ROM
from time import time_ns

PIXEL_SCALE = 4
width, height = 256 * PIXEL_SCALE, 240 * PIXEL_SCALE


class PyNesWindow(Tk):
    def __init__(self):
        super().__init__()
        self.cpu = None
        self.ppu = None

        self.canvas = Canvas(self, height=height, width=width)
        self.canvas.pack()

        self.image = PhotoImage(width=width, height=height)

        self.title("Testee")
        self.frame = GameFrame()
        self.last_frame = GameFrame()
        self.last_frame_time = time_ns()

        menu = Menu(self)
        self.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open Rom", command=self.open_rom)
        file_menu.add_command(label="Exit", command=self.quit)

        print("Finish setup Tkinter")

    def pause(self):
        print("pause")
        if self.cpu is not None:
            self.cpu.running = False

    def open_rom(self):
        self.pause()
        file_name = filedialog.askopenfilename()
        print(file_name)
        with open(file_name, 'rb') as file:
            rom_bytes = file.read()

            rom = ROM(rom_bytes)
            ram = RAM()
            self.ppu = PPU(rom.chr_rom, rom.screen_mirroring)
            io_regs = IO_Registers()
            bus = Bus(ram, self.ppu, io_regs, rom)
            self.cpu = CPU(bus)
            self.cpu.start_up(self.update_ui, self.handle_joystick_input)
            self.cpu.run_rom(rom)

    def update_ui(self):
        a = time_ns()
        self.ppu.render(self.frame)
        print("PPU:", (time_ns() - a) / 10**9)

        for x in range(GameFrame.WIDTH):
            for y in range(GameFrame.HEIGHT):
                color_index = y * GameFrame.WIDTH + x
                new_color = self.frame.data[color_index]
                old_color = self.last_frame.data[color_index]

                if new_color != old_color:
                    print(new_color)
                    self.image.put("#%02x%02x%02x" % new_color, (y, x))
                    # self.canvas.create_rectangle(
                    #     x * PIXEL_SCALE, y * PIXEL_SCALE, x * (PIXEL_SCALE + 1), y * (PIXEL_SCALE + 1),
                    #     fill=("#%02x%02x%02x" % new_color),
                    #     outline=""
                    # )
                    self.canvas.create_image(0, 0, image=self.image)

        self.last_frame.data = self.frame.data[:]

        current_time = time_ns()
        diff = current_time - self.last_frame_time
        self.last_frame_time = current_time
        # print("update_ui total time: {}".format((time_ns() - a) / 10**9))
        print("FPS: {}. Time since last frame: {}".format(10**9 / diff, diff / 10**9))

    def handle_joystick_input(self):
        pass
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_UP:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.UP
        #         elif event.key == pygame.K_LEFT:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.LEFT
        #         elif event.key == pygame.K_DOWN:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.DOWN
        #         elif event.key == pygame.K_RIGHT:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.RIGHT
        #         elif event.key == pygame.K_z:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.BUTTON_A
        #         elif event.key == pygame.K_x:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.BUTTON_B
        #         elif event.key == pygame.K_a:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.START
        #         elif event.key == pygame.K_s:
        #             self.io_regs.joypad1.button_status |= Joypad.JoypadButton.SELECT
        #
        #     elif event.type == pygame.KEYUP:
        #         if event.key == pygame.K_UP:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.UP
        #         elif event.key == pygame.K_LEFT:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.LEFT
        #         elif event.key == pygame.K_DOWN:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.DOWN
        #         elif event.key == pygame.K_RIGHT:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.RIGHT
        #         elif event.key == pygame.K_z:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.BUTTON_A
        #         elif event.key == pygame.K_x:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.BUTTON_B
        #         elif event.key == pygame.K_a:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.START
        #         elif event.key == pygame.K_s:
        #             self.io_regs.joypad1.button_status &= 0xFF - Joypad.JoypadButton.SELECT
        #
        #     elif event.type == pygame.QUIT:
        #         self.cpu.running = False
        #         sys.exit()


def main():
    window = PyNesWindow()
    window.mainloop()


if __name__ == '__main__':
    main()
