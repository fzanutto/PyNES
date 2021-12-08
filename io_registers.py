from memory_owner import MemoryOwner


class IO_Registers(MemoryOwner):
    def __init__(self):
        super().__init__(0x4000, 0x401F)
