from memory_owner import MemoryOwnerMixin


class PPU(MemoryOwnerMixin, object):
    memory_start_location = 0x2000
    memory_end_location = 0x2007

    def __init__(self):
        self.memory: list[int] = [0]*8

    def get_memory(self) -> list[int]:
        return self.memory
