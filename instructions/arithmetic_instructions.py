

from addressing import ImmediateReadAddressing
from instructions.generic_instructions import Instruction


class And(Instruction):
    identifier_byte = bytes([0x29])
    sets_zero_bit = True
    sets_negative_bit = True


class AndImm(ImmediateReadAddressing, And):

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = cpu.a_reg & value
