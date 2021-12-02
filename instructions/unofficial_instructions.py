

from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, AbsoluteAddressingWithY, ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX, ZeroPageAddressingWithY
from instructions.base_instructions import Ld
from instructions.generic_instructions import Instruction


class Lax(Ld):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value
        cpu.x_reg = value


class LaxZeroPage(ZeroPageAddressing, Lax):
    identifier_byte = bytes([0xA7])

class LaxZeroPageY(ZeroPageAddressingWithY, Lax):
    identifier_byte = bytes([0xB7])


class LaxAbs(AbsoluteAddressing, Lax):
    identifier_byte = bytes([0xAF])

class LaxAbsWithY(AbsoluteAddressingWithY, Lax):
    identifier_byte = bytes([0xBF])


class LaxIndexedIndirect(IndexedIndirectAddressing, Lax):
    identifier_byte = bytes([0xA3])

class LaxIndIdx(IndirectIndexedAddressing, Lax):
    identifier_byte = bytes([0xB3])



