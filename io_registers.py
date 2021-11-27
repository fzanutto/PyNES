from memory_owner import MemoryOwnerMixin


class IO_Registers(MemoryOwnerMixin, object):
    memory_start_location = 0x4000
    memory_end_location = 0x401F

    def __init__(self):
        self.memory: list[int] = [0] * 32

    def get_memory(self) -> list[int]:
        return self.memory
