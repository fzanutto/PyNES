from typing import Optional
import cpu as c


class Addressing:
    data_length = 0

    @classmethod
    def get_instruction_length(cls):
        return cls.data_length + 1

    @classmethod
    def get_offset(cls, cpu):
        return 0


class XRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.x_reg


class YRegOffset(object):
    @classmethod
    def get_offset(cls, cpu):
        return cpu.y_reg


class ImplicitAddressing(Addressing):
    """
    instructions that have no data passed
    example: CLD
    """
    data_length = 0

    @classmethod
    def get_address(cls, cpu, data_bytes) -> Optional[int]:
        return None


class ImmediateReadAddressing(Addressing):
    """
    read a value from the instruction data
    example: STA #7
    example: 8D 07
    """
    data_length = 1

    @classmethod
    def get_data(cls, cpu, memory_address, data_bytes):
        return data_bytes[0]


class AbsoluteAddressing(Addressing):
    """
    looks up an absolute memory address and returns the value
    example: STA $12 34
    example: 8D 34 12
    """
    data_length = 2

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        return int.from_bytes(data_bytes, byteorder='little') + cls.get_offset(cpu)


class AbsoluteAddressingWithX(XRegOffset, AbsoluteAddressing):
    """
    adds the x reg offset to an absolute memory location
    """


class AbsoluteAddressingWithY(YRegOffset, AbsoluteAddressing):
    """
    adds the y reg offset to an absolute memory location
    """


class ZeroPageAddressing(Addressing):
    """
    look up an absolute memory address in the first 256 bytes
    example: STA $12
    memory_address: $12
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        address = int.from_bytes(
            data_bytes, byteorder='little') + cls.get_offset(cpu)

        # % 256 for overflow
        return address % 256


class ZeroPageAddressingWithX(XRegOffset, ZeroPageAddressing):
    """
    adds the x reg offset to an absolute memory address in the first 256 bytes
    """


class ZeroPageAddressingWithY(YRegOffset, ZeroPageAddressing):
    """
    adds the x reg offset to an absolute memory address in the first 256 bytes
    """


class RelativeAddressing(Addressing):
    """
    offset from current PC, can only jump 128 bytes in either direction
    """
    data_length = 1

    @classmethod
    def get_address(cls, cpu, data_bytes: bytes) -> Optional[int]:
        # get the PC
        current_address = cpu.pc_reg

        # offset from the following instruction
        return current_address + 2 + int.from_bytes(data_bytes, byteorder='little')


class IndirectBase(Addressing):
    @classmethod
    def get_address(cls, cpu: 'c.CPU', data_bytes):
        # look up the bytes at [base_address, base_address + 1]
        original_location = super().get_address(cpu, data_bytes)

        lsb = cpu.get_memory(original_location)
        msb = cpu.get_memory(original_location + 1)

        return msb * 256 + lsb


class IndirectAddressing(IndirectBase, AbsoluteAddressing):
    """
    indirect address
    """

# TODO: bug with get_offset being reused


class IndexedIndirectAddressing(IndirectBase, ZeroPageAddressingWithX):
    """
    adds the x reg before indirection
    """


class IndirectIndexedAddressing(IndirectBase, ZeroPageAddressing):
    """
    adds the y reg after indirection
    """
    @classmethod
    def get_address(cls, cpu: 'c.CPU', data_bytes):
        return super().get_address(cpu, data_bytes) + cpu.y_reg
