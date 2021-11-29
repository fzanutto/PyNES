

from typing import Optional
from addressing import ImplicitAddressing
from instructions.generic_instructions import Instruction


class Tax(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xAA])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value
class Tay(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xA8])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value

class Tsx(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xBA])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.sp_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value
class Txa(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x8A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.x_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

class Txs(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x9A])
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.x_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.sp_reg = value

class Tya(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x98])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.y_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class PushToStack(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.set_memory(0x0100 + cpu.sp_reg, value, num_bytes=1)
        cpu.increase_stack_size(1)


class Php(ImplicitAddressing, PushToStack):
    identifier_byte = bytes([0x08])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.status_reg.to_int() | (1 << 5) | (1 << 4)


class Pha(ImplicitAddressing, PushToStack):
    identifier_byte = bytes([0x48])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.a_reg


class PullFromStack(Instruction):

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        cpu.decrease_stack_size(1)
        return cpu.get_memory(0x0100 + cpu.sp_reg)


class Pla(ImplicitAddressing, PullFromStack):
    identifier_byte = bytes([0x68])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Plp(ImplicitAddressing, PullFromStack):
    '''
    Pulls value from stack pointer and sets status register
    This instruction does not change the value of bits 4 and 5 of the status register
    '''
    identifier_byte = bytes([0x28])

    @classmethod
    def write(cls, cpu, memory_address, value):
        current_value = cpu.status_reg.to_int()
        bits_4_5 = current_value & ((1 << 5) | (1 << 4))
        remove_bits_4_5 = (~((1 << 5) | (1 << 4))) & 255
        cpu.status_reg.from_int((value & remove_bits_4_5) | bits_4_5)
