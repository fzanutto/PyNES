from addressing import AbsoluteAddressing, ZeroPageAddressing, ZeroPageAddressingWithY, ZeroPageAddressingWithX, \
    AbsoluteAddressingWithX, AbsoluteAddressingWithY, IndirectIndexedAddressing, IndexedIndirectAddressing
from instructions.base_instructions import Sta, Stx, Sty


# Store A

class StaZeroPage(ZeroPageAddressing, Sta):
    identifier_byte = bytes([0x85])

    @classmethod
    def get_cycles(cls):
        return 3


class StaZeroPageX(ZeroPageAddressingWithX, Sta):
    identifier_byte = bytes([0x95])

    @classmethod
    def get_cycles(cls):
        return 4


class StaAbs(AbsoluteAddressing, Sta):
    identifier_byte = bytes([0x8D])

    @classmethod
    def get_cycles(cls):
        return 4

class StaAbsWithX(AbsoluteAddressingWithX, Sta):
    identifier_byte = bytes([0x9D])

    @classmethod
    def get_cycles(cls):
        return 5


class StaAbsWithY(AbsoluteAddressingWithY, Sta):
    identifier_byte = bytes([0x99])

    @classmethod
    def get_cycles(cls):
        return 5


class StaIndX(IndexedIndirectAddressing, Sta):
    identifier_byte = bytes([0x81])

    @classmethod
    def get_cycles(cls):
        return 6


class StaIndY(IndirectIndexedAddressing, Sta):
    identifier_byte = bytes([0x91])

    @classmethod
    def get_cycles(cls):
        return 6


# Store X
class StxZeroPage(ZeroPageAddressing, Stx):
    identifier_byte = bytes([0x86])
    
    @classmethod
    def get_cycles(cls):
        return 3


class StxAbs(AbsoluteAddressing, Stx):
    identifier_byte = bytes([0x8E])
    
    @classmethod
    def get_cycles(cls):
        return 4


class StxZeroPageY(ZeroPageAddressingWithY, Stx):
    identifier_byte = bytes([0x96])


# Store Y
class StyZeroPage(ZeroPageAddressing, Sty):
    identifier_byte = bytes([0x84])


class StyAbs(AbsoluteAddressing, Sty):
    identifier_byte = bytes([0x8C])


class StyZeroPageX(ZeroPageAddressingWithX, Sty):
    identifier_byte = bytes([0x94])
