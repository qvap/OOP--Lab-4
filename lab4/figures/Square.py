from figures.Rectangle import CRectangle

class CSquare(CRectangle): # Базовый класс квадрата
    def __init__(self, master, canvas, x, y):
        super().__init__(master, canvas, x, y)

        self._size = [100.0, 100.0]