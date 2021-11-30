from typing import Optional
from addressing import ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, ZeroPageAddressing
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


class AndIdxInd(IndexedIndirectAddressing, And):
    identifier_byte = bytes([0x21])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        mem_value = cpu.get_memory(memory_address)

        return mem_value & cpu.a_reg


class AndZeroPage(ZeroPageAddressing, And):
    identifier_byte = bytes([0x25])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        mem_value = cpu.get_memory(memory_address)

        return mem_value & cpu.a_reg


class Cmp(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.a_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = diff & (1 << 7)


class CmpImm(ImmediateReadAddressing, Cmp):
    identifier_byte = bytes([0xC9])


class CmpIdxInd(IndexedIndirectAddressing, Cmp):
    identifier_byte = bytes([0xC1])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)


class CmpZeroPage(ZeroPageAddressing, Cmp):
    identifier_byte = bytes([0xC5])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)


class Cpy(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.y_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = diff & (1 << 7)


class CpyImm(ImmediateReadAddressing, Cpy):
    identifier_byte = bytes([0xC0])


class Cpx(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.x_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (
            diff & (1 << 7)) > 0


class CpxImm(ImmediateReadAddressing, Cpx):
    identifier_byte = bytes([0xE0])


class CpxZeroPage(ZeroPageAddressing, Cpx):
    identifier_byte = bytes([0XE4])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)


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


class Lsr(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x4A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = value >> 1

        return value

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Asl(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x0A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 0

        value = (value << 1) & 255

        return value

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ror(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x6A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = (value >> 1) | (current_carry << 7)

        return value

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Rol(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x2A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 1

        value = ((value << 1) | current_carry) & 255

        return value

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ora(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class OraImm(ImmediateReadAddressing, Ora):
    identifier_byte = bytes([0x09])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        mem_value = super().get_data(cpu, memory_address, data_bytes)

        return mem_value | cpu.a_reg


class OraIdxInd(IndexedIndirectAddressing, Ora):
    identifier_byte = bytes([0x01])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        mem_value = cpu.get_memory(memory_address)

        return mem_value | cpu.a_reg


class OraZeroPage(ZeroPageAddressing, Ora):
    identifier_byte = bytes([0x05])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        mem_value = cpu.get_memory(memory_address)

        return mem_value | cpu.a_reg


class Eor(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class EorImm(ImmediateReadAddressing, Eor):
    identifier_byte = bytes([0x49])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ super().get_data(cpu, memory_address, data_bytes)


class EorIdxInd(IndexedIndirectAddressing, Eor):
    identifier_byte = bytes([0x41])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ cpu.get_memory(memory_address)


class EorZeroPage(ZeroPageAddressing, Eor):
    identifier_byte = bytes([0x45])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ cpu.get_memory(memory_address)
