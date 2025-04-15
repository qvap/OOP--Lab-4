from figures.BaseFigure import Figure

class CCircle(Figure): # Базовый класс круга

    def __init__(self, master, canvas, x, y):
        super().__init__(master=master, x=x, y=y, canvas=canvas)

        # Private
        self._radius = self._size // 2

    def draw(self): # Отрисовывает круг на Canvas
        super().draw()
        self.canvas.create_oval(self._x - self._radius, self._y - self._radius,\
            self._x + self._radius, self._y + self._radius, fill = self._color, width = 5, outline = self._chosen_border_color)

    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри круга
        return ((x - self._x)**2 + (y - self._y)**2) <= self._radius**2
    
    def boundaries(self, x: int, y: int, canvas_width: int, canvas_height: int) -> bool:
        return self._radius <= x <= canvas_width - self._radius and \
               self._radius <= y <= canvas_height - self._radius

    def move(self, x: int, y: int):
        super().move(x, y)
        self._x = self.constrain(self._radius, self.canvas.winfo_width() - self._radius, self._x)
        self._y = self.constrain(self._radius, self.canvas.winfo_height() - self._radius, self._y)