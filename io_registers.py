from joypad import Joypad
from memory_owner import MemoryOwner


class IO_Registers(MemoryOwner):
    def __init__(self):
        super().__init__(0x4000, 0x401F)
        self.joypad1 = Joypad()
        self.joypad2 = Joypad()

    def get(self, position: int):
        if position == 0x4016:
            return self.joypad1.read()
        elif position == 0x4017:
            return self.joypad2.read()

        return super().get(position)

    def set(self, position: int, value: int, size: int):
        if position == 0x4016:
            self.joypad1.write(value)
            self.joypad2.write(value)
            return

        super().set(position, value)
