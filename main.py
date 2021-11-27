import argparse

from cpu import CPU
from io_registers import IO_Registers
from ram import RAM
from ppu import PPU
from rom import ROM


def main():
    # set up command line argument parser
    parser = argparse.ArgumentParser(description='NES Emulator.')
    parser.add_argument('rom_path',
                        metavar='rom_path',
                        type=str,
                        help='path to rom')
    args = parser.parse_args()

    # load rom
    with open(args.rom_path, 'rb') as file:
        rom_bytes = file.read()

    rom = ROM(rom_bytes)

    # create ram
    ram = RAM()

    # create ppu
    ppu = PPU()

    io_regs = IO_Registers()

    # create cpu
    cpu = CPU(ram, ppu, io_regs)
    cpu.start_up()
    cpu.run_rom(rom)


if __name__ == '__main__':
    main()
