from typing import Optional
from addressing import ImplicitAddressing, RelativeAddressing
from instructions.generic_instructions import Instruction, WritesToMem


class Jmp(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.push_to_stack(cpu.pc_reg - 1, 2)

        # jump to the memory location
        super().write(cpu, memory_address, value)


class BranchSet(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        if cpu.status_reg.bits[cls.bit]:
            cls.add_cycle_from_branch = 1
            super().write(cpu, memory_address, value)
        else:
            cls.add_cycle_from_branch = 0


class BranchClear(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        if not cpu.status_reg.bits[cls.bit]:
            cls.add_cycle_from_branch = 1
            super().write(cpu, memory_address, value)
        else:
            cls.add_cycle_from_branch = 0


class Ld(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True
    
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.bus.read_memory(memory_address)


class Lda(Ld):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class Ldx(Ld):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.x_reg = value


class Ldy(Ld):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.y_reg = value


class Sta(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes: bytes):
        return cpu.a_reg


class Stx(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.x_reg


class Sty(WritesToMem, Instruction):
    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.y_reg


class SetBit(ImplicitAddressing, Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.status_reg.bits[cls.bit] = True


class ClearBit(ImplicitAddressing, Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        cpu.status_reg.bits[cls.bit] = False
