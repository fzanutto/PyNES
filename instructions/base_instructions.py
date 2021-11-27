from addressing import ImplicitAddressing, RelativeAddressing
from instructions.generic_instructions import Instruction, WritesToMem


class Jmp(Instruction):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.pc_reg = memory_address


class Jsr(Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.increase_stack_size(2)

        # store de pc reg on the stack
        cpu.set_memory(cpu.sp_reg, cpu.pc_reg, num_bytes=2)

        # jump to the memory location
        super().write(cpu, memory_address, value)


class BranchSet(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        if cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class BranchClear(RelativeAddressing, Jmp):
    @classmethod
    def write(cls, cpu, memory_address, value):
        if not cpu.status_reg.bits[cls.bit]:
            super().write(cpu, memory_address, value)


class Nop(Instruction):
    pass


class Ld(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True


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
    """
    sets a bit to be True
    """
    @classmethod
    def apply_side_effects(cls, cpu):
        cpu.status_reg.bits[cls.bit] = True


class ClearBit(ImplicitAddressing, Instruction):
    """
    sets a bit to be False
    """
    @classmethod
    def apply_side_effects(cls, cpu):
        cpu.status_reg.bits[cls.bit] = False


class Transfer(ImplicitAddressing, Instruction):
    """
    transfer value from a register to another
    """
    fromRegister = None
    toRegister = None

    @classmethod
    def apply_side_effects(cls, cpu):
        if cls.fromRegister is None or cls.toRegister is None:
            raise Exception('Transfer instruction register is None',
                            cls.fromRegister, cls.toRegister)

        if cls.fromRegister == "X":
            if cls.toRegister == "S":
                cpu.sp_reg = cpu.x_reg
