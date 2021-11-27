from addressing import AbsoluteAddressing, ImplicitAddressing, IndirectAddressing
from instructions.base_instructions import Jmp, Jsr, BranchSet, BranchClear
from instructions.generic_instructions import Instruction
from status import Status


class JmpAbs(AbsoluteAddressing, Jmp):
    identifier_byte = bytes([0x4C])


class JmpInd(IndirectAddressing, Jmp):
    identifier_byte = bytes([0x6C])


class JsrAbs(AbsoluteAddressing, Jsr):
    identifier_byte = bytes([0x20])


class Rts(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x60])

    @classmethod
    def write(cls, cpu, memory_address, value):

        value1 = cpu.get_memory(cpu.sp_reg)
        value2 = cpu.get_memory(cpu.sp_reg + 1)

        cpu.decrease_stack_size(2)

        cpu.pc_reg = (value2 << 8) + value1


# branch sets
class Bcs(BranchSet):
    identifier_byte = bytes([0xB0])
    bit = Status.StatusTypes.carry


class Bmi(BranchSet):
    identifier_byte = bytes([0x30])
    bit = Status.StatusTypes.negative


class Beq(BranchSet):
    identifier_byte = bytes([0xF0])
    bit = Status.StatusTypes.zero


class Bvs(BranchSet):
    identifier_byte = bytes([0x70])
    bit = Status.StatusTypes.overflow


# branch clear
class Bcc(BranchClear):
    identifier_byte = bytes([0x90])
    bit = Status.StatusTypes.carry


class Bpl(BranchClear):
    identifier_byte = bytes([0x10])
    bit = Status.StatusTypes.negative


class Bvc(BranchClear):
    identifier_byte = bytes([0x50])
    bit = Status.StatusTypes.overflow


class Bne(BranchClear):
    identifier_byte = bytes([0xD0])
    bit = Status.StatusTypes.zero
