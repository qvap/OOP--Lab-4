from figures.BaseFigure import Figure

class CCircle(Figure): # Базовый класс круга

    def __init__(self, master, canvas, x, y):
        super().__init__(master, canvas, x, y)

        # Private
        self._radius = self._size[0] // 2

    def draw(self, draw_border: bool): # Отрисовывает круг на Canvas
        super().draw(draw_border)
        self._radius = self._size[0] // 2
        self.canvas.create_oval(self._x - self._radius, self._y - self._radius,\
            self._x + self._radius, self._y + self._radius, fill = self._color, width = 5, outline = self._chosen_border_color)

    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри круга
        return ((x - self._x)**2 + (y - self._y)**2) <= self._radius**2