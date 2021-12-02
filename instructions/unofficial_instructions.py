

from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, AbsoluteAddressingWithY, ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX, ZeroPageAddressingWithY
from instructions.arithmetic_instructions import Sbc
from instructions.base_instructions import Ld
from instructions.generic_instructions import Instruction
from status import Status


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


class Sax(Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:

        return cpu.a_reg & cpu.x_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.set_memory(memory_address, value, num_bytes=1)


class SaxZeroPage(ZeroPageAddressing, Sax):
    identifier_byte = bytes([0x87])


class SaxZeroPageY(ZeroPageAddressingWithY, Sax):
    identifier_byte = bytes([0x97])


class SaxAbs(AbsoluteAddressing, Sax):
    identifier_byte = bytes([0x8F])


class SaxIdxInd(IndexedIndirectAddressing, Sax):
    identifier_byte = bytes([0x83])


class SbcNop(ImmediateReadAddressing, Sbc):
    identifier_byte = bytes([0xEB])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)
        value = (~value) & 255

        return super().sub_carry(cpu, memory_address, data_bytes, value)


class Dcp(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = value >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = value == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (
            value & (1 << 7)) > 0

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        value = cpu.get_memory(memory_address)
        return value - 1 if value > 0 else 255


class DcpZeroPage(ZeroPageAddressing, Dcp):
    identifier_byte = bytes([0xC7])


class DcpZeroPageX(ZeroPageAddressingWithX, Dcp):
    identifier_byte = bytes([0xD7])


class DcpAbs(AbsoluteAddressing, Dcp):
    identifier_byte = bytes([0xCF])


class DcpAbsX(AbsoluteAddressingWithX, Dcp):
    identifier_byte = bytes([0xDF])


class DcpAbsY(AbsoluteAddressingWithY, Dcp):
    identifier_byte = bytes([0xDB])


class DcpIdxInd(IndexedIndirectAddressing, Dcp):
    identifier_byte = bytes([0xC3])


class DcpIndIdx(IndirectIndexedAddressing, Dcp):
    identifier_byte = bytes([0xD3])
