class Figure(): # Общий класс фигуры
    def __init__(self, master, canvas, x, y):
        # Protected
        self._container = master
        self._size = 100.0
        self._color =self._container.chosen_color
        self._border_color = "#ffffff"
        self._selected = False
        self._x = x
        self._y = y

        # vvv Нужны для передвижения фигур мышкой
        self._offset_x = 0
        self._offset_y = 0

        # Public
        self.canvas = canvas

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

    def measure_offsets(self, x: int, y: int): # Вычисляет относ. положение фигуры от мыши
        self._offset_x = self._x - x
        self._offset_y = self._y - y

    def boundaries(self, x: int, y: int, canvas_width: int, canvas_height: int) -> bool: # Переопред. в классе
        return True

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