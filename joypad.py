class Joypad:

    class JoypadButton: 
        RIGHT             = 0b10000000
        LEFT              = 0b01000000
        DOWN              = 0b00100000
        UP                = 0b00010000
        START             = 0b00001000
        SELECT            = 0b00000100
        BUTTON_B          = 0b00000010
        BUTTON_A          = 0b00000001
       

    def __init__(self):
        self.strobe = False
        self.button_index = 0
        self.button_status = 0

    def write(self, data: int):
        self.strobe = data & 1
        if self.strobe:
            self.button_index = 0

    def read(self):
        if self.button_index > 7:
            return 1
        
        result = (self.button_status & (1 << self.button_index)) >> self.button_index
        if not self.strobe and self.button_index <= 7:
            self.button_index += 1

        return result