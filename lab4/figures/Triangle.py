from figures.BaseFigure import Figure

class CTriangle(Figure):
    def __init__(self, master, canvas, x, y):
        super().__init__(master, canvas, x, y)

        # Private
        self.__triangle_points = [[],[],[]]
        self.update_points()

    def draw(self):
        super().draw()
        self.update_points()
        points = [coordinate for point in self.__triangle_points for coordinate in point] # раскрытие вложенности
        self.canvas.create_polygon(points, fill = self._color, width = 5, outline = self._chosen_border_color)
    
    def update_points(self):
        self.__triangle_points = [[self._x - (self.size[0] // 2), self._y + (self.size[1] // 2)],\
                                 [self._x, self._y - (self.size[1] // 2)],\
                                 [self._x + (self.size[0] // 2), self._y + (self.size[1] // 2)]]
        
    def sign(self, number: float) -> int: # проверяет знак
        if number < 0:
            return -1
        elif number > 0:
            return 1
        return 0

    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри треугольника
        # Укорочение переменных для удобства
        x1 = self.__triangle_points[0][0]
        y1 = self.__triangle_points[0][1]
        x2 = self.__triangle_points[1][0]
        y2 = self.__triangle_points[1][1]
        x3 = self.__triangle_points[2][0]
        y3 = self.__triangle_points[2][1]

        # Считаются псевдоскалярные произведения
        check_first_side = (x1 - x)*(y2 - y1) - (x2 - x1)*(y1 - y)
        check_second_side = (x2 - x)*(y3 - y2) - (x3 - x2)*(y2 - y)
        check_third_side = (x3 - x)*(y1 - y3) - (x1 - x3)*(y3 - y)

        # True, если все знаки равны или хотя бы одно значение равно нулю
        return ((self.sign(check_first_side) == self.sign(check_second_side) == self.sign(check_third_side))\
                or (check_first_side*check_second_side*check_third_side == 0))