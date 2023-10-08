
class MemoryOwner:

    def __init__(self, mem_start: int, mem_end: int):
        self.memory_start_location = mem_start
        self.memory_end_location = mem_end
        self.memory = [0] * (mem_end - mem_start)

    def get_memory(self) -> list[int]:
        return self.memory

    def get(self, position: int) -> int:
        return self.get_memory()[position - self.memory_start_location]

    def get_bytes(self, position: int, size: int = 1) -> bytes:
        initial_position = position - self.memory_start_location

        value = self.get_memory()[initial_position: initial_position + size]

        return bytes(value)

    def set(self, position: int, value: int, size: int = 1):
        """
        sets int at given position
        """
        for i in range(size):
            self.get_memory()[position - self.memory_start_location + i] = (value >> (8*i)) & 255
