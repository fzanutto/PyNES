class Frame:
    WIDTH = 256
    HEIGHT = 240

    def __init__(self) -> None:
        self.data = [
            [(0, 0, 0) for _ in range(Frame.HEIGHT)] for _ in range(Frame.WIDTH)
        ]

    def set_pixel(self, x: int, y: int, rgb: tuple[int, int, int]):
        if x < Frame.WIDTH and y < Frame.HEIGHT:
            self.data[x][y] = rgb
