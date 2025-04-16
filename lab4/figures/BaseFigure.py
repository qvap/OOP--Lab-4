class Figure(): # Общий класс фигуры
    def __init__(self, master, canvas, x, y):
        # Protected
        self._container = master
        self._size_coef = 1.0
        self._size_x = 100.0
        self._size_y = 100.0
        self._color =self._container.chosen_color
        self._border_color = "#ffffff"
        self._selected = False
        self._x, self._y = x, y

        # vvv Нужны для передвижения фигур мышкой
        self._offset_x, self._offset_y = 0, 0

        # vvv Нужны для скейлинга
        self._startmouse_x, self._startmouse_y = x, y

        # Public
        self.canvas = canvas
        self.size = [self._size_x * self._size_coef, self._size_y * self._size_coef]

        self._chosen_border_color = ""

        print(f"New point: {x}, {y}")
    
    def draw(self): # Переопред. в классе
        self._chosen_border_color = self._border_color if self._selected else self._color

    def select(self):
        self._selected = True

    def deselect(self):
        self._selected = False
    
    def mousecheck(self, x: int, y: int): # Переопред. в классе
        pass

    def set_size_coef(self, size_coef: float):
        self._size_coef = size_coef
        self.size = [self._size_x * self._size_coef, self._size_y * self._size_coef]

    def measure_offsets(self, x: int, y: int): # Вычисляет относ. положение фигуры от мыши
        self._offset_x = self._x - x
        self._offset_y = self._y - y

    def boundaries(self, x: int, y: int, size_x: float, size_y: float, canvas_width: int, canvas_height: int) -> bool: # опред. границ
        return (size_x // 2) <= x <= canvas_width - (size_x // 2) and \
               (size_y // 2) <= y <= canvas_height - (size_y // 2)

    def constrain(self, lower_limit:int, upper_limit:int, value:int) -> int: # не даёт значению выйти за границы
        if value < lower_limit:
            return lower_limit
        if value > upper_limit:
            return upper_limit
        return value

    def destroy(self) -> bool:
        if self._selected:
            del self
            return True
        return False