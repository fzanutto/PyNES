from addressing import ImplicitAddressing
from instructions.generic_instructions import Instruction


class Tax(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xAA])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Tay(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xA8])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Tsx(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xBA])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.sp_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Txa(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x8A])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.x_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Txs(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x9A])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.x_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.sp_reg = value


class Tya(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x98])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.y_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class PushToStack(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.push_to_stack(value, 1)


class Php(ImplicitAddressing, PushToStack):
    identifier_byte = bytes([0x08])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.status_reg.to_int() | (1 << 5) | (1 << 4)

    @classmethod
    def get_cycles(cls):
        return 3


class Pha(ImplicitAddressing, PushToStack):
    identifier_byte = bytes([0x48])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.a_reg

    @classmethod
    def get_cycles(cls):
        return 3


class PullFromStack(Instruction):

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> int:
        return cpu.pull_from_stack(1)


class Pla(ImplicitAddressing, PullFromStack):
    identifier_byte = bytes([0x68])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    @classmethod
    def get_cycles(cls):
        return 4


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

    @classmethod
    def get_cycles(cls):
        return 4
