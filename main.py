import argparse
from bus import Bus
from cpu import CPU
from io_registers import IO_Registers
from ram import RAM
from ppu.ppu import PPU
from rom import ROM
from ui import UI

def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='rom_path',
                        type=str,
                        help='path to rom',
                        default='',
                        nargs='?')

    parser.add_argument('--debug', dest='debug', const=True, default=False, help='logs the running program', nargs='?')
    parser.add_argument('--nestest', dest='nestest', const=True, default=False, help='runs nestest rom', nargs='?')
    args = parser.parse_args()

    if args.nestest:
        args.debug = True
        with open('nestest.nes', 'rb') as file:
            rom_bytes = file.read()
    else:
        with open(args.rom_path, 'rb') as file:
            rom_bytes = file.read()

    rom = ROM(rom_bytes)

    # create ram
    ram = RAM()

    # create ppu
    ppu = PPU(rom.chr_rom, rom.screen_mirroring)

    io_regs = IO_Registers()

    bus = Bus(ram, ppu, io_regs, rom)

    # create cpu
    cpu = CPU(bus, args.debug, args.nestest)
    
    ui = UI(cpu, ppu)

    cpu.start_up(ui.handle_and_update_ui)
    cpu.run_rom(rom)


if __name__ == '__main__':
    main()
