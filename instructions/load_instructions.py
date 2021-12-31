from typing import Optional
from addressing import ImmediateReadAddressing, IndexedIndirectAddressing, ZeroPageAddressing, AbsoluteAddressing, \
    IndirectIndexedAddressing, ZeroPageAddressingWithX, ZeroPageAddressingWithY, AbsoluteAddressingWithY, \
    AbsoluteAddressingWithX
from instructions.base_instructions import Ldx, Lda, Ldy


# Load X
class LdxImm(ImmediateReadAddressing, Ldx):
    identifier_byte = bytes([0xA2])
    
    @classmethod
    def get_cycles(cls):
        return 2


class LdxZeroPage(ZeroPageAddressing, Ldx):
    identifier_byte = bytes([0xA6])
    
    @classmethod
    def get_cycles(cls):
        return 3


class LdxZeroPageY(ZeroPageAddressingWithY, Ldx):
    identifier_byte = bytes([0xB6])


class LdxAbs(AbsoluteAddressing, Ldx):
    identifier_byte = bytes([0xAE])
    
    @classmethod
    def get_cycles(cls):
        return 4


class LdxAbsY(AbsoluteAddressingWithY, Ldx):
    identifier_byte = bytes([0xBE])
    
    @classmethod
    def get_cycles(cls):
        return 4


# Load A
class LdaIndexedIndirect(IndexedIndirectAddressing, Lda):
    identifier_byte = bytes([0xA1])


class LdaZeroPage(ZeroPageAddressing, Lda):
    identifier_byte = bytes([0xA5])


class LdaImm(ImmediateReadAddressing, Lda):
    identifier_byte = bytes([0xA9])


class LdaAbs(AbsoluteAddressing, Lda):
    identifier_byte = bytes([0xAD])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.bus.read_memory(memory_address)

    @classmethod
    def get_cycles(cls):
        return 4


class LdaIndIdx(IndirectIndexedAddressing, Lda):
    identifier_byte = bytes([0xB1])


class LdaZeroPageX(ZeroPageAddressingWithX, Lda):
    identifier_byte = bytes([0xB5])


class LdaAbsWithY(AbsoluteAddressingWithY, Lda):
    identifier_byte = bytes([0xB9])


class LdaAbsWithX(AbsoluteAddressingWithX, Lda):
    identifier_byte = bytes([0xBD])


# Load Y
class LdyImm(ImmediateReadAddressing, Ldy):
    identifier_byte = bytes([0xA0])


class LdyZeroPage(ZeroPageAddressing, Ldy):
    identifier_byte = bytes([0xA4])


class LdyZeroPageX(ZeroPageAddressingWithX, Ldy):
    identifier_byte = bytes([0xB4])


class LdyAbs(AbsoluteAddressing, Ldy):
    identifier_byte = bytes([0xAC])


class LdyAbsX(AbsoluteAddressingWithX, Ldy):
    identifier_byte = bytes([0xBC])
