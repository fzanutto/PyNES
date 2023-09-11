from typing import Optional
from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, AbsoluteAddressingWithY, ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
from instructions.generic_instructions import Instruction, WritesToMem
from status import Status


class Sbc(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    def sub_carry(cpu, value):
        is_first_number_positive = cpu.a_reg < 128
        is_second_number_positive = value < 128

        sub = cpu.a_reg + value + \
            int(cpu.status_reg.bits[Status.StatusTypes.carry])

        cpu.status_reg.bits[Status.StatusTypes.carry] = sub > 255

        sub = sub % 256

        is_sum_positive = sub < 128

        if is_first_number_positive == is_second_number_positive:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = is_first_number_positive != is_sum_positive
        else:
            cpu.status_reg.bits[Status.StatusTypes.overflow] = False

        return sub

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)
        value = (~value) & 255

        return cls.sub_carry(cpu, value)


class SbcImm(ImmediateReadAddressing, Sbc):
    identifier_byte = bytes([0xE9])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)
        value = (~value) & 255

        return super().sub_carry(cpu, value)


class SbcZeroPage(ZeroPageAddressing, Sbc):
    identifier_byte = bytes([0xE5])


class SbcZeroPageX(ZeroPageAddressingWithX, Sbc):
    identifier_byte = bytes([0xF5])


class SbcAbs(AbsoluteAddressing, Sbc):
    identifier_byte = bytes([0xED])


class SbcAbsY(AbsoluteAddressingWithY, Sbc):
    identifier_byte = bytes([0xF9])


class SbcAbsX(AbsoluteAddressingWithX, Sbc):
    identifier_byte = bytes([0xFD])


class SbcIdxInd(IndexedIndirectAddressing, Sbc):
    identifier_byte = bytes([0xE1])


class SbcIndIdx(IndirectIndexedAddressing, Sbc):
    identifier_byte = bytes([0xF1])


class Adc(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    def add_carry(cpu, memory_address, dat_bytes, value):
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
    def get_data(cls, cpu, memory_address, data_bytes):
        value = cpu.bus.read_memory(memory_address)

        return cls.add_carry(cpu, memory_address, data_bytes, value)


class AdcImm(ImmediateReadAddressing, Adc):
    identifier_byte = bytes([0x69])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)

        return super().add_carry(cpu, memory_address, data_bytes, value)


class AdcIdxInd(IndexedIndirectAddressing, Adc):
    identifier_byte = bytes([0x61])


class AdcIndIdx(IndirectIndexedAddressing, Adc):
    identifier_byte = bytes([0x71])


class AdcZeroPage(ZeroPageAddressing, Adc):
    identifier_byte = bytes([0x65])


class AdcZeroPageX(ZeroPageAddressingWithX, Adc):
    identifier_byte = bytes([0x75])


class AdcAbs(AbsoluteAddressing, Adc):
    identifier_byte = bytes([0x6D])


class AdcAbsY(AbsoluteAddressingWithY, Adc):
    identifier_byte = bytes([0x79])


class AdcAbsX(AbsoluteAddressingWithX, Adc):
    identifier_byte = bytes([0x7D])


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


class Inc(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return (cpu.bus.read_memory(memory_address) + 1) % 256


class IncZeroPage(ZeroPageAddressing, Inc):
    identifier_byte = bytes([0xE6])

    @classmethod
    def get_cycles(cls):
        return 5


class IncZeroPageX(ZeroPageAddressingWithX, Inc):
    identifier_byte = bytes([0xF6])

    @classmethod
    def get_cycles(cls):
        return 6


class IncAbs(AbsoluteAddressing, Inc):
    identifier_byte = bytes([0xEE])

    @classmethod
    def get_cycles(cls):
        return 6


class IncAbsX(AbsoluteAddressingWithX, Inc):
    identifier_byte = bytes([0xFE])

    @classmethod
    def get_cycles(cls):
        return 7


class Dec(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)
        return value - 1 if value > 0 else 255


class DecZeroPage(ZeroPageAddressing, Dec):
    identifier_byte = bytes([0xC6])

    @classmethod
    def get_cycles(cls):
        return 5


class DecZeroPageX(ZeroPageAddressingWithX, Dec):
    identifier_byte = bytes([0xD6])

    @classmethod
    def get_cycles(cls):
        return 6


class DecAbs(AbsoluteAddressing, Dec):
    identifier_byte = bytes([0xCE])

    @classmethod
    def get_cycles(cls):
        return 6


class DecAbsX(AbsoluteAddressingWithX, Dec):
    identifier_byte = bytes([0xDE])

    @classmethod
    def get_cycles(cls):
        return 7
