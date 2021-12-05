

from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, AbsoluteAddressingWithY, ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX, ZeroPageAddressingWithY
from instructions.arithmetic_instructions import Sbc
from instructions.base_instructions import Ld
from instructions.generic_instructions import Instruction, WritesToMem
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


class Dcp(WritesToMem, Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        value = cpu.a_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = value >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = value == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (value & (1 << 7)) > 0

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


class Isb(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        mem_value = (cpu.get_memory(memory_address) + 1) % 256
        cpu.set_memory(memory_address, mem_value)

        mem_value = (~mem_value) & 255

        return cls.sub_carry(cpu, memory_address, data_bytes, mem_value)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    def sub_carry(cpu, memory_address, data_bytes, value):
        is_first_number_positive = cpu.a_reg < 128
        is_second_number_positive = value < 128

        sub = cpu.a_reg + value + int(cpu.status_reg.bits[Status.StatusTypes.carry])

        cpu.status_reg.bits[Status.StatusTypes.carry] = sub > 255

        sub = sub % 256

        is_sum_positive = sub < 128

        if is_first_number_positive == is_second_number_positive:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = is_first_number_positive != is_sum_positive
        else:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = False

        return sub


class IsbZeroPage(ZeroPageAddressing, Isb):
    identifier_byte = bytes([0xE7])


class IsbZeroPageX(ZeroPageAddressingWithX, Isb):
    identifier_byte = bytes([0xF7])


class IsbAbs(AbsoluteAddressing, Isb):
    identifier_byte = bytes([0xEF])


class IsbAbsX(AbsoluteAddressingWithX, Isb):
    identifier_byte = bytes([0xFF])


class IsbAbsY(AbsoluteAddressingWithY, Isb):
    identifier_byte = bytes([0xFB])


class IsbIdxInd(IndexedIndirectAddressing, Isb):
    identifier_byte = bytes([0xE3])


class IsbIndIdx(IndirectIndexedAddressing, Isb):
    identifier_byte = bytes([0xF3])


class Slo(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    def asl(cpu, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 0
        value = (value << 1) & 255
        return value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        value = cpu.get_memory(memory_address)
        value = cls.asl(cpu, value)

        cpu.set_memory(memory_address, value, num_bytes=1)

        return value | cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class SloZeroPage(ZeroPageAddressing, Slo):
    identifier_byte = bytes([0x07])


class SloZeroPageX(ZeroPageAddressingWithX, Slo):
    identifier_byte = bytes([0x17])


class SloAbsolute(AbsoluteAddressing, Slo):
    identifier_byte = bytes([0x0F])


class SloAbsoluteX(AbsoluteAddressingWithX, Slo):
    identifier_byte = bytes([0x1F])


class SloAbsoluteY(AbsoluteAddressingWithY, Slo):
    identifier_byte = bytes([0x1B])


class SloIdxInd(IndexedIndirectAddressing, Slo):
    identifier_byte = bytes([0x03])


class SloIndIdx(IndirectIndexedAddressing, Slo):
    identifier_byte = bytes([0x13])


class Rla(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        value = cpu.get_memory(memory_address)

        value = cls.rol(cpu, value)

        cpu.set_memory(memory_address, value)

        return cpu.a_reg & value

    def rol(cpu, value):
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 1

        value = ((value << 1) | current_carry) & 255

        return value

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class RlaZeroPage(ZeroPageAddressing, Rla):
    identifier_byte = bytes([0x27])


class RlaZeroPageX(ZeroPageAddressingWithX, Rla):
    identifier_byte = bytes([0x37])


class RlaAbsolute(AbsoluteAddressing, Rla):
    identifier_byte = bytes([0x2F])


class RlaAbsoluteX(AbsoluteAddressingWithX, Rla):
    identifier_byte = bytes([0x3F])


class RlaAbsoluteY(AbsoluteAddressingWithY, Rla):
    identifier_byte = bytes([0x3B])


class RlaIdxInd(IndexedIndirectAddressing, Rla):
    identifier_byte = bytes([0x23])


class RlaIndIdx(IndirectIndexedAddressing, Rla):
    identifier_byte = bytes([0x33])


class Sre(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    def lsr(cpu, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = value >> 1

        return value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        value = cpu.get_memory(memory_address)
        value = cls.lsr(cpu, value)

        cpu.set_memory(memory_address, value)

        return cpu.a_reg ^ value


class SreZeroPage(ZeroPageAddressing, Sre):
    identifier_byte = bytes([0x47])


class SreZeroPageX(ZeroPageAddressingWithX, Sre):
    identifier_byte = bytes([0x57])


class SreAbsolute(AbsoluteAddressing, Sre):
    identifier_byte = bytes([0x4F])


class SreAbsoluteX(AbsoluteAddressingWithX, Sre):
    identifier_byte = bytes([0x5F])


class SreAbsoluteY(AbsoluteAddressingWithY, Sre):
    identifier_byte = bytes([0x5B])


class SreIdxInd(IndexedIndirectAddressing, Sre):
    identifier_byte = bytes([0x43])


class SreIndIdx(IndirectIndexedAddressing, Sre):
    identifier_byte = bytes([0x53])


class Rra(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        value = cpu.get_memory(memory_address)

        value = cls.ror(cpu, value)

        cpu.set_memory(memory_address, value)

        return cls.add_carry(cpu, value)

    def ror(cpu, value):
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = (value >> 1) | (current_carry << 7)

        return value

    def add_carry(cpu, value):
        is_first_number_positive = cpu.a_reg < 128
        is_second_number_positive = value < 128

        sum = cpu.a_reg + value + \
            int(cpu.status_reg.bits[Status.StatusTypes.carry])

        cpu.status_reg.bits[Status.StatusTypes.carry] = sum > 255

        sum = sum % 256

        is_sum_positive = sum < 128

        if is_first_number_positive == is_second_number_positive:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = is_first_number_positive != is_sum_positive
        else:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = False

        return sum

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class RraZeroPage(ZeroPageAddressing, Rra):
    identifier_byte = bytes([0x67])


class RraZeroPageX(ZeroPageAddressingWithX, Rra):
    identifier_byte = bytes([0x77])


class RraAbsolute(AbsoluteAddressing, Rra):
    identifier_byte = bytes([0x6F])


class RraAbsoluteX(AbsoluteAddressingWithX, Rra):
    identifier_byte = bytes([0x7F])


class RraAbsoluteY(AbsoluteAddressingWithY, Rra):
    identifier_byte = bytes([0x7B])


class RraIdxInd(IndexedIndirectAddressing, Rra):
    identifier_byte = bytes([0x63])


class RraIndIdx(IndirectIndexedAddressing, Rra):
    identifier_byte = bytes([0x73])
