class Frame:
    WIDTH = 256
    HEIGHT = 240

    def __init__(self) -> None:
        self.data = [(0,0,0)] * Frame.WIDTH * Frame.HEIGHT

    def set_pixel(self, x: int, y: int, rgb: tuple[3]):
        position = y * Frame.WIDTH + x
        if position < len(self.data):
            self.data[position] = rgb
