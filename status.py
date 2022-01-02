from collections import OrderedDict
from enum import Enum

from instructions.generic_instructions import Instruction


class Status:
    """
    7  bit  0
    ---- ----
    NVss DIZC
    |||| ||||
    |||| |||+- Carry: 1 if last addition or shift resulted in a carry, or if
    |||| |||     last subtraction resulted in no borrow
    |||| ||+-- Zero: 1 if last operation resulted in a 0 value
    |||| |+--- Interrupt: Interrupt inhibit
    |||| |       (0: /IRQ and /NMI get through; 1: only /NMI gets through)
    |||| +---- Decimal: 1 to make ADC and SBC use binary-coded decimal arithmetic
    ||||         (ignored on second-source 6502 like that in the NES)
    ||++------ s: No effect, used by the stack copy, see note below
    |+-------- Overflow: 1 if last ADC or SBC resulted in signed overflow,
    |            or D6 from last BIT
    +--------- Negative: Set to bit 7 of the last operation
    """

    class StatusTypes(Enum):
        carry = 0  # C
        zero = 1  # Z
        interrupt = 2  # I
        decimal = 3  # D
        break1 = 4
        break2 = 5
        overflow = 6  # V
        negative = 7  # N

    def __init__(self):
        self.bits = OrderedDict([
            (Status.StatusTypes.carry, False),
            (Status.StatusTypes.zero, False),
            (Status.StatusTypes.interrupt, True),
            (Status.StatusTypes.decimal, False),
            (Status.StatusTypes.break1, False),
            (Status.StatusTypes.break2, True),
            (Status.StatusTypes.overflow, False),
            (Status.StatusTypes.negative, False),
        ])

    def update(self, instruction: Instruction, value: int):
        """
        update the status based on the instruction attributes and the valye calculated
        """
        if instruction.sets_zero_bit:
            self.bits[Status.StatusTypes.zero] = value == 0
        if instruction.sets_negative_bit:
            self.bits[Status.StatusTypes.negative] = value > 127

    def to_int(self) -> int:
        value = 0
        for i, bit in enumerate(self.bits.values()):
            value += int(bit) << i
        return value

    def from_int(self, value: int):
        for i in self.bits:
            self.bits[i] = (value & (1 << i.value)) > 0

    def copy(self):
        status = Status()
        status.from_int(self.to_int())
        return status