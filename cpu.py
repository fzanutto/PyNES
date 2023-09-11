from time import time_ns
from bus import Bus
from instructions.generic_instructions import Instruction
from rom import ROM
from status import Status

import instructions.instructions as i_file
import instructions.jump_instructions as j_file
import instructions.load_instructions as l_file
import instructions.store_instructions as s_file
import instructions.stack_instructions as t_file
import instructions.arithmetic_instructions as a_file
import instructions.logical_instructions as log_file
import instructions.nop_instructions as n_file
import instructions.unofficial_instructions as u_file


class CPU:
    def __init__(self, bus: Bus, debug: bool = False, nes_test: bool = False):
        self.rom = None
        self.bus = bus
        self.debug = debug
        self.nes_test = nes_test
        self.cycle = 7  # debug variable to use nestest
        
        # status register: store a single byte
        self.status_reg: Status = Status()

        # counter registers: store a single byte
        self.pc_reg: int = 0  # program counter
        self.sp_reg: int = 0  # stack pointer

        # data registers: store a single byte
        self.x_reg: int = 0  # x register
        self.y_reg: int = 0  # y register
        self.a_reg: int = 0  # a register

        self.running: bool = True

        # create the instructions that the cpu can interpret
        instructions_list = self.find_instructions(Instruction)
        self.instructions: dict[bytes, Instruction] = {}
        for instruction in instructions_list:
            if instruction.identifier_byte in self.instructions.keys():
                raise Exception('Duplicate instruction identifier bytes ' + instruction.identifier_byte.hex())
            self.instructions[instruction.identifier_byte] = instruction

    def start_up(self, update_ui_callback, handle_input_callback):
        """
        set the initial values of cpu registers
        status reg: 000100 (irqs disabled)
        x, y, a regs: 0
        stack pointer: $FD
        $4017: 0 (frame irq disabled)
        $4015: 0 (sound channels disabled)
        $4000-$400F: 0 (sound registers)
        """

        self.bus.update_ui_callback = update_ui_callback
        self.bus.joystick_input_callback = handle_input_callback

        self.pc_reg = 0
        self.status_reg = Status()  # know as 'P' on NesDev Wiki
        self.sp_reg = 0xFD

        self.x_reg = 0
        self.y_reg = 0
        self.a_reg = 0

    def push_to_stack(self, value, size):
        for i in range(size):
            self.bus.write_memory(0x0100 + self.sp_reg, (value >> (8 * (size - i - 1))) & 255, num_bytes=1)
            self.sp_reg -= 1

    def pull_from_stack(self, size):
        value = 0

        for i in range(size):
            self.sp_reg += 1
            value += self.bus.read_memory(0x0100 + self.sp_reg) << (8 * i)

        return value

    def find_instructions(self, cls) -> list[Instruction]:
        subclasses = [subc for subc in cls.__subclasses__() if subc.identifier_byte is not None]
        return subclasses + [g for s in cls.__subclasses__() for g in self.find_instructions(s)]

    def run_rom(self, rom: ROM):
        self.rom = rom
        self.pc_reg = 0xC000 if self.nes_test else 0x8000  # first rom address

        # run program
        self.running = True
        last_time = time_ns()
        
        while self.running:
            if self.bus.get_nmi_status():
                self.push_to_stack(self.pc_reg, 2)

                status_reg_copy = self.status_reg.copy()
                status_reg_copy.bits[Status.StatusTypes.break1] = 0
                status_reg_copy.bits[Status.StatusTypes.break2] = 1

                self.push_to_stack(status_reg_copy.to_int(), 1)

                self.status_reg.bits[Status.StatusTypes.interrupt] = 1

                self.bus.tick(2)
                self.pc_reg = int.from_bytes(self.bus.read_memory_bytes(0xFFFA, 2), byteorder='little')

            # get the current byte at pc
            identifier_byte = bytes([self.bus.read_memory(self.pc_reg)])

            # turn the byte into an Instruction
            instruction: Instruction = self.instructions.get(identifier_byte)

            # get the data bytes
            data_bytes = self.bus.read_memory_bytes(self.pc_reg + 1, instruction.data_length)

            if self.debug:
                self.debug_print(self.pc_reg, identifier_byte, data_bytes, instruction)

            self.pc_reg += instruction.get_instruction_length()

            value = instruction.execute(self, data_bytes)

            instr_cycles = instruction.get_cycles()

            self.cycle += instr_cycles

            self.status_reg.update(instruction, value)

            self.bus.tick(instr_cycles)

            cur_time = time_ns()

            # print('time spent this cpu instruction: {} - {}'.format((cur_time - last_time) / 10**9, instruction))

            if self.debug and cur_time - last_time > 0:
                print('time spent this cpu instruction', (cur_time - last_time) / 10**9)

            last_time = cur_time

    def debug_print(self, pc_reg: int, identifier_byte, data_bytes, instruction: Instruction):
        # print out diagnostic information
        # example: C000  4C F5 C5  JMP $C5F5      A:00 X:00 Y:00 P:24 SP:FD PPU:  0,  0 CYC:

        registers_state = [
            hex(self.a_reg)[2:].upper(),
            hex(self.x_reg)[2:].upper(),
            hex(self.y_reg)[2:].upper(),
            hex(self.status_reg.to_int())[2:].upper(),
            hex(self.sp_reg)[2:].upper()
        ]

        inst_bytes = (identifier_byte + data_bytes).hex().upper()
        rng = range(0, len(inst_bytes), 2)
        inst_hexes = [inst_bytes[i:i + 2] for i in rng]

        print("{:0>4}  {:<8}  {:<31} A:{:0>2} X:{:0>2} Y:{:0>2} P:{:0>2} SP:{} CYC:{}".format(
            hex(pc_reg)[2:].upper(),
            ' '.join(inst_hexes),
            instruction.__name__[0:3].upper(),
            *registers_state,
            self.cycle
        ))
