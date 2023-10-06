class Frame:
    WIDTH = 256
    HEIGHT = 240

    def __init__(self) -> None:
        self.data = [(0,0,0)] * Frame.WIDTH * Frame.HEIGHT
        self.pixels_to_update = []

    def set_pixel(self, x: int, y: int, rgb: tuple[int, int, int]):
        position = y * Frame.WIDTH + x
        if position < 256 * 240:
            if self.data[position] != rgb:
                self.data[position] = rgb
                self.pixels_to_update.append([x, y, rgb])
