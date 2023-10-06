class GameFrame:
    WIDTH = 256
    HEIGHT = 240

    def __init__(self) -> None:
        self.data = [(0, 0, 0)] * GameFrame.WIDTH * GameFrame.HEIGHT

    def set_pixel(self, x: int, y: int, rgb: list[int]):
        position = y * GameFrame.WIDTH + x
        if position < 256 * 240:
            self.data[position] = rgb
