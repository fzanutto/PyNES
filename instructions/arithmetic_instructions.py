from typing import Optional
from addressing import ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
from instructions.generic_instructions import Instruction
from status import Status


class Sbc(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    def sub_carry(cpu, memory_address, dat_bytes, value):
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


class SbcImm(ImmediateReadAddressing, Sbc):
    identifier_byte = bytes([0xE9])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)
        value = (~value) & 255

        return super().sub_carry(cpu, memory_address, data_bytes, value)


class SbcIdxInd(IndexedIndirectAddressing, Sbc):
    identifier_byte = bytes([0xE1])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.get_memory(memory_address)
        value = (~value) & 255

        return super().sub_carry(cpu, memory_address, data_bytes, value)


class SbcZeroPage(ZeroPageAddressing, Sbc):
    identifier_byte = bytes([0xE5])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.get_memory(memory_address)
        value = (~value) & 255

        return super().sub_carry(cpu, memory_address, data_bytes, value)


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


class AdcImm(ImmediateReadAddressing, Adc):
    identifier_byte = bytes([0x69])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = super().get_data(cpu, memory_address, data_bytes)

        return super().add_carry(cpu, memory_address, data_bytes, value)


class AdcIdxInd(IndexedIndirectAddressing, Adc):
    identifier_byte = bytes([0x61])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = cpu.get_memory(memory_address)

        return super().add_carry(cpu, memory_address, data_bytes, value)


class AdcZeroPage(ZeroPageAddressing, Adc):
    identifier_byte = bytes([0x65])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        value = cpu.get_memory(memory_address)

        return super().add_carry(cpu, memory_address, data_bytes, value)


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
