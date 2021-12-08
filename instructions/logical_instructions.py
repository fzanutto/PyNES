from typing import Optional
from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, AbsoluteAddressingWithY, ImmediateReadAddressing, ImplicitAddressing, IndexedIndirectAddressing, IndirectIndexedAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
from instructions.generic_instructions import Instruction, WritesToMem
from status import Status


class And(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        mem_value = cpu.bus.read_memory(memory_address)

        return mem_value & cpu.a_reg


class AndImm(ImmediateReadAddressing, And):
    identifier_byte = bytes([0x29])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg & super().get_data(cpu, memory_address, data_bytes)


class AndIdxInd(IndexedIndirectAddressing, And):
    identifier_byte = bytes([0x21])


class AndIndIdx(IndirectIndexedAddressing, And):
    identifier_byte = bytes([0x31])


class AndZeroPage(ZeroPageAddressing, And):
    identifier_byte = bytes([0x25])


class AndZeroPageX(ZeroPageAddressingWithX, And):
    identifier_byte = bytes([0x35])


class AndAbs(AbsoluteAddressing, And):
    identifier_byte = bytes([0x2D])


class AndAbsX(AbsoluteAddressingWithX, And):
    identifier_byte = bytes([0x3D])


class AndAbsY(AbsoluteAddressingWithY, And):
    identifier_byte = bytes([0x39])


class Cmp(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.a_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (diff & (1 << 7)) > 0

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.bus.read_memory(memory_address)


class CmpImm(ImmediateReadAddressing, Cmp):
    identifier_byte = bytes([0xC9])


class CmpZeroPage(ZeroPageAddressing, Cmp):
    identifier_byte = bytes([0xC5])


class CmpZeroPageX(ZeroPageAddressingWithX, Cmp):
    identifier_byte = bytes([0xD5])


class CmpAbs(AbsoluteAddressing, Cmp):
    identifier_byte = bytes([0xCD])


class CmpAbsX(AbsoluteAddressingWithX, Cmp):
    identifier_byte = bytes([0xDD])


class CmpAbsY(AbsoluteAddressingWithY, Cmp):
    identifier_byte = bytes([0xD9])


class CmpIdxInd(IndexedIndirectAddressing, Cmp):
    identifier_byte = bytes([0xC1])


class CmpIndIdx(IndirectIndexedAddressing, Cmp):
    identifier_byte = bytes([0xD1])


class Cpy(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.y_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (diff & (1 << 7)) > 0

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.bus.read_memory(memory_address)


class CpyImm(ImmediateReadAddressing, Cpy):
    identifier_byte = bytes([0xC0])


class CpyZeroPage(ZeroPageAddressing, Cpy):
    identifier_byte = bytes([0xC4])


class CpyAbs(AbsoluteAddressing, Cpy):
    identifier_byte = bytes([0xCC])


class Cpx(Instruction):
    @classmethod
    def apply_side_effects(cls, cpu, memory_address, value):
        diff = cpu.x_reg - value
        cpu.status_reg.bits[Status.StatusTypes.carry] = diff >= 0
        cpu.status_reg.bits[Status.StatusTypes.zero] = diff == 0
        cpu.status_reg.bits[Status.StatusTypes.negative] = (
            diff & (1 << 7)) > 0

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return cpu.bus.read_memory(memory_address)


class CpxImm(ImmediateReadAddressing, Cpx):
    identifier_byte = bytes([0xE0])


class CpxZeroPage(ZeroPageAddressing, Cpx):
    identifier_byte = bytes([0XE4])


class CpxAbs(AbsoluteAddressing, Cpx):
    identifier_byte = bytes([0XEC])


class Lsr(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    def lsr(cpu, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = value >> 1

        return value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)
        return cls.lsr(cpu, value)


class LsrImpl(ImplicitAddressing, Lsr):
    identifier_byte = bytes([0x4A])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        return super().lsr(cpu, cpu.a_reg)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class LsrZeroPage(ZeroPageAddressing, Lsr):
    identifier_byte = bytes([0x46])


class LsrZeroPageX(ZeroPageAddressingWithX, Lsr):
    identifier_byte = bytes([0x56])


class LsrAbs(AbsoluteAddressing, Lsr):
    identifier_byte = bytes([0x4E])


class LsrAbsX(AbsoluteAddressingWithX, Lsr):
    identifier_byte = bytes([0x5E])


class Asl(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    def asl(cpu, value):
        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 0
        value = (value << 1) & 255
        return value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)
        return cls.asl(cpu, value)


class AslImpl(ImplicitAddressing, Asl):
    identifier_byte = bytes([0x0A])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg
        return super().asl(cpu, value)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class AslZeroPage(ZeroPageAddressing, Asl):
    identifier_byte = bytes([0x06])


class AslZeroPageX(ZeroPageAddressingWithX, Asl):
    identifier_byte = bytes([0x16])


class AslAbs(AbsoluteAddressing, Asl):
    identifier_byte = bytes([0x0E])


class AslAbsX(AbsoluteAddressingWithX, Asl):
    identifier_byte = bytes([0x1E])


class Ror(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)

        return cls.ror(cpu, value)

    def ror(cpu, value):
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & 0x1

        value = (value >> 1) | (current_carry << 7)

        return value


class RorImpl(ImplicitAddressing, Ror):
    identifier_byte = bytes([0x6A])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg
        return super().ror(cpu, value)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class RorZeroPage(ZeroPageAddressing, Ror):
    identifier_byte = bytes([0x66])


class RorZeroPageX(ZeroPageAddressingWithX, Ror):
    identifier_byte = bytes([0x76])


class RorAbs(AbsoluteAddressing, Ror):
    identifier_byte = bytes([0x6E])


class RorAbsX(AbsoluteAddressingWithX, Ror):
    identifier_byte = bytes([0x7E])


class Rol(WritesToMem, Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.bus.read_memory(memory_address)

        return cls.rol(cpu, value)

    def rol(cpu, value):
        current_carry = cpu.status_reg.bits[Status.StatusTypes.carry]

        cpu.status_reg.bits[Status.StatusTypes.carry] = value & (1 << 7) > 1

        value = ((value << 1) | current_carry) & 255

        return value


class RolImp(ImplicitAddressing, Rol):
    identifier_byte = bytes([0x2A])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes) -> Optional[int]:
        value = cpu.a_reg

        return cls.rol(cpu, value)

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class RolZeroPage(ZeroPageAddressing, Rol):
    identifier_byte = bytes([0x26])


class RolZeroPageX(ZeroPageAddressingWithX, Rol):
    identifier_byte = bytes([0x36])


class RolAbs(AbsoluteAddressing, Rol):
    identifier_byte = bytes([0x2E])


class RolAbsX(AbsoluteAddressingWithX, Rol):
    identifier_byte = bytes([0x3E])


class Ora(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        mem_value = cpu.bus.read_memory(memory_address)

        return mem_value | cpu.a_reg

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value


class OraImm(ImmediateReadAddressing, Ora):
    identifier_byte = bytes([0x09])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        mem_value = super().get_data(cpu, memory_address, data_bytes)

        return mem_value | cpu.a_reg


class OraZeroPage(ZeroPageAddressing, Ora):
    identifier_byte = bytes([0x05])


class OraZeroPageX(ZeroPageAddressingWithX, Ora):
    identifier_byte = bytes([0x15])


class OraAbs(AbsoluteAddressing, Ora):
    identifier_byte = bytes([0x0D])


class OraAbsY(AbsoluteAddressingWithY, Ora):
    identifier_byte = bytes([0x19])


class OraAbsX(AbsoluteAddressingWithX, Ora):
    identifier_byte = bytes([0x1D])


class OraIdxInd(IndexedIndirectAddressing, Ora):
    identifier_byte = bytes([0x01])


class OraIndIdx(IndirectIndexedAddressing, Ora):
    identifier_byte = bytes([0x11])


class Eor(Instruction):
    sets_zero_bit = True
    sets_negative_bit = True

    @classmethod
    def write(cls, cpu, memory_address, value):
        cpu.a_reg = value

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ cpu.bus.read_memory(memory_address)


class EorImm(ImmediateReadAddressing, Eor):
    identifier_byte = bytes([0x49])

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return cpu.a_reg ^ super().get_data(cpu, memory_address, data_bytes)


class EorIdxInd(IndexedIndirectAddressing, Eor):
    identifier_byte = bytes([0x41])


class EorIndIdx(IndirectIndexedAddressing, Eor):
    identifier_byte = bytes([0x51])


class EorZeroPage(ZeroPageAddressing, Eor):
    identifier_byte = bytes([0x45])


class EorZeroPageX(ZeroPageAddressingWithX, Eor):
    identifier_byte = bytes([0x55])


class EorAbsolute(AbsoluteAddressing, Eor):
    identifier_byte = bytes([0x4D])


class EorAbsoluteY(AbsoluteAddressingWithY, Eor):
    identifier_byte = bytes([0x59])


class EorAbsoluteX(AbsoluteAddressingWithX, Eor):
    identifier_byte = bytes([0x5D])
