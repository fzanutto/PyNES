

from addressing import AbsoluteAddressing, AbsoluteAddressingWithX, ImmediateReadAddressing, ImplicitAddressing, ZeroPageAddressing, ZeroPageAddressingWithX
from instructions.generic_instructions import Instruction

# Implicit

class Nop1A(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x1A])

class Nop3A(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x3A])

class Nop5A(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x5A])

class Nop7A(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0x7A])

class NopDA(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xDA])

class NopFA(ImplicitAddressing, Instruction):
    identifier_byte = bytes([0xFA])



# Immediate

class Nop80(ImmediateReadAddressing, Instruction):
    identifier_byte = bytes([0x80])

class Nop82(ImmediateReadAddressing, Instruction):
    identifier_byte = bytes([0x82])

class Nop89(ImmediateReadAddressing, Instruction):
    identifier_byte = bytes([0x89])

class NopC2(ImmediateReadAddressing, Instruction):
    identifier_byte = bytes([0xC2])

class NopE2(ImmediateReadAddressing, Instruction):
    identifier_byte = bytes([0xE2])


# ZeroPage

class Nop04(ZeroPageAddressing, Instruction):
    identifier_byte = bytes([0x04])

class Nop44(ZeroPageAddressing, Instruction):
    identifier_byte = bytes([0x44])


class Nop64(ZeroPageAddressing, Instruction):
    identifier_byte = bytes([0x64])

# ZeroPageX

class Nop14(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0x14])

class Nop34(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0x34])

class Nop54(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0x54])

class Nop74(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0x74])

class NopD4(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0xD4])

class NopF4(ZeroPageAddressingWithX, Instruction):
    identifier_byte = bytes([0xF4])


# Absolute

class Nop0C(AbsoluteAddressing, Instruction):
    identifier_byte = bytes([0x0C])

# Absolute X

class Nop1C(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0x1C])

class Nop3C(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0x3C])

class Nop5C(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0x5C])

class Nop7C(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0x7C])

class NopDC(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0xDC])

class NopFC(AbsoluteAddressingWithX, Instruction):
    identifier_byte = bytes([0xFC])
