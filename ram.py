from memory_owner import MemoryOwner


class RAM(MemoryOwner):
    '''
    $0000 - $07FF -> Game RAM
    $0800 - $0FFF -> Mirror of $0000-$07FF
    $1000 - $17FF -> Mirror of $0000-$07FF
    $1800 - $1FFF   -> Mirror of $0000-$07FF
    '''

    def __init__(self):
        super().__init__(0x0000, 0x1FFF)
