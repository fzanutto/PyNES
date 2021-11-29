

from typing import Optional
from addressing import ImplicitAddressing
from instructions.base_instructions import Transfer
from instructions.generic_instructions import Instruction


class Txs(Transfer):
    identifier_byte = bytes([0x9A])
    fromRegister = "X"
    toRegister = "S"


class Tsx(Transfer):
    indetifier_byte = bytes([0xBA])
    fromRegister = "S"
    toRegister = "X"


class PushToStack(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.increase_stack_size(1)
        cpu.set_memory(cpu.sp_reg, value, num_bytes=1)


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
    def get_address(cls, cpu, data_bytes) -> Optional[int]:
        return cpu.sp_reg

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.get_memory(memory_address)

    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.decrease_stack_size(1)


class Pla(ImplicitAddressing, PullFromStack):
    identifier_byte = bytes([0x68])

    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Plp(ImplicitAddressing, PullFromStack):
    identifier_byte = bytes([0x28])

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.status_reg.from_int(value)
