from addressing import *
from instructions.base_instructions import SetBit, ClearBit, Nop
from instructions.generic_instructions import Instruction
from status import Status


# Nop
class NopImp(ImplicitAddressing, Nop):
    identifier_byte = bytes([0xEA])


# set status instructions
class Sec(SetBit):
    identifier_byte = bytes([0x38])
    bit = Status.StatusTypes.carry


class Sei(SetBit):
    identifier_byte = bytes([0x78])
    bit = Status.StatusTypes.interrupt


class Sed(SetBit):
    identifier_byte = bytes([0xF8])
    bit = Status.StatusTypes.decimal


# clear status instructions
class Cld(ClearBit):
    identifier_byte = bytes([0xD8])
    bit = Status.StatusTypes.decimal


class Clc(ClearBit):
    identifier_byte = bytes([0x18])
    bit = Status.StatusTypes.carry


class Clv(ClearBit):
    identifier_byte = bytes([0xB8])
    bit = Status.StatusTypes.overflow


class Cli(ClearBit):
    identifier_byte = bytes([0x58])
    bit = Status.StatusTypes.interrupt


class BitZeroPage(ZeroPageAddressing, Instruction):
    identifier_byte = bytes([0x24])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)

    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        and_result = cpu.a_reg & value

        cpu.status_reg.bits[Status.StatusTypes.zero] = not and_result
        cpu.status_reg.bits[Status.StatusTypes.overflow] = (
            value & (1 << 6)) > 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (
            value & (1 << 7)) > 0


class Php(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x08])

    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.increase_stack_size(1)

        cpu.set_memory(cpu.sp_reg, cpu.status_reg.to_int(), num_bytes=1)


class Pla(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x68])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_address(cls, cpu, data_bytes) -> Optional[int]:
        return cpu.sp_reg

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.decrease_stack_size(1)
