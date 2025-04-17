from figures.BaseFigure import Figure

class CRectangle(Figure): # Базовый класс прямоугольника
    def __init__(self, master, canvas, x, y):
        super().__init__(master, canvas, x, y)
        
        # Private
        self.__half_size_x, self.__half_size_y = 0, 0

        self._size_x = 100.0
        self._size_y = 50.0
        self.update_size()
    
    def draw(self):
        super().draw()
        self.__half_size_x = self.size[0] // 2
        self.__half_size_y = self.size[1] // 2
        self.canvas.create_rectangle(self._x - self.__half_size_x,
                                     self._y - self.__half_size_y,
                                     self._x + self.__half_size_x,
                                     self._y + self.__half_size_y,
                                     fill = self._color, width = 5, outline = self._chosen_border_color)
    
    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри прямоугольника
        return (self._x - self.__half_size_x <= x <= self._x + self.__half_size_x) and \
            (self._y - self.__half_size_y <= y <= self._y + self.__half_size_y)