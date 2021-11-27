from memory_owner import MemoryOwnerMixin

KB = 1024


class RAM(MemoryOwnerMixin, object):
    '''
    $0000 - $07FF -> Game RAM
    $0800 - $0FFF -> Mirror of $0000-$07FF
    $1000 - $17FF -> Mirror of $0000-$07FF
    $1800 - $1FFF   -> Mirror of $0000-$07FF
    '''
    memory_start_location = 0x0000
    memory_end_location = 0x1FFF

    def __init__(self):
        self.memory: list[int] = [0]*KB*2

    def get_memory(self) -> list[int]:
        return self.memory
