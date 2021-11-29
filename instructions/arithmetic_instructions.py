

from typing import Optional
from addressing import AbsoluteAddressing, ImmediateReadAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
from instructions.generic_instructions import Instruction
from status import Status


class And(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class AndImm(ImmediateReadAddressing, And):
    identifier_byte = bytes([0x29])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg & super().get_data(cpu, memory_address, data_bytes)


class Cmp(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.a_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = cpu.a_reg >= 0x80


class CmpImm(ImmediateReadAddressing, Cmp):
    identifier_byte = bytes([0xC9])


class Or(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.a_reg | value


class OrImm(ImmediateReadAddressing, Or):
    identifier_byte = bytes([0x09])


class Xor(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class XorImm(ImmediateReadAddressing, Xor):
    identifier_byte = bytes([0x49])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ super().get_data(cpu, memory_address, data_bytes)
