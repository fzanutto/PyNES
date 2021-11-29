

from typing import Optional
from addressing import AbsoluteAddressing, ImmediateReadAddressing, ImplicitAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
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
        cpu.status_reg.bits[Status.StatusTypes.negative] = diff & (1 << 7)


class CmpImm(ImmediateReadAddressing, Cmp):
    identifier_byte = bytes([0xC9])


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
        cpu.status_reg.bits[Status.StatusTypes.negative] = diff & (1 << 7)


class CpxImm(ImmediateReadAddressing, Cpx):
    identifier_byte = bytes([0xE0])


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


class SubCarry(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

class SubCarryImm(ImmediateReadAddressing, SubCarry):
    identifier_byte = bytes([0xE9])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)
        value = (~value) & 255

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


class AddCarry(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class AddCarryImm(ImmediateReadAddressing, AddCarry):
    identifier_byte = bytes([0x69])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)
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


class Iny(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xC8])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return (cpu.y_reg + 1) % 256

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value

class Dey(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x88])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.y_reg - 1 if cpu.y_reg > 0 else 255

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value

class Inx(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xE8])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return (cpu.x_reg + 1) % 256

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value

class Dex(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xCA])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.x_reg - 1 if cpu.x_reg > 0 else 255

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value