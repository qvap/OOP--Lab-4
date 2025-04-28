from Tools import Tools

class Figure(): # Общий класс фигуры
    def __init__(self, master, canvas, x, y):
        # Protected
        self._container = master
        self._size = [100.0, 100.0]
        self._color =self._container.chosen_color
        self._border_color = "#ffffff"
        self._x, self._y = x, y

        # vvv Нужны для передвижения фигур мышкой
        self._offset_x, self._offset_y = 0, 0

        # vvv Нужны для скейлинга
        self._startmouse_x, self._startmouse_y = x, y

        # Public
        self.canvas = canvas

        self._chosen_border_color = ""

        print(f"New point: {x}, {y}")
    
    def draw(self, draw_border: bool): # Переопред. в классе
        self._chosen_border_color = self._border_color if draw_border else self._color

    def move(self, x: int, y: int):
        self._x = x
        self._y = y
    
    def resize(self, new_size): # Изменяет размер фигуры
        self._size = new_size
    
    def pass_coordinates(self) -> list: # Возвращает координаты фигуры
        return (self._x, self._y)
    
    def pass_size(self) -> list: # Возвращает размер фигуры
        return self._size
    
    def mousecheck(self, x: int, y: int): # Переопред. в классе
        pass

    def measure_offsets(self, x: int, y: int): # Вычисляет относ. положение фигуры от мыши
        self._offset_x = self._x - x
        self._offset_y = self._y - y

    def boundaries(self, x: int, y: int, size_x: float, size_y: float, canvas_width: int, canvas_height: int) -> bool: # опред. границ
        return (size_x // 2) <= x <= canvas_width - (size_x // 2) and \
               (size_y // 2) <= y <= canvas_height - (size_y // 2)
    
    def check_outside(self):
        frame_width = self.canvas.winfo_width()
        frame_height = self.canvas.winfo_height()
        if not self.boundaries(self._x, self._y, self._size[0], self._size[1], frame_width, frame_height):
            self.move(Tools.clamp(self._x, frame_width - (self._size[0] // 2), self._size[0] // 2),
                      Tools.clamp(self._y, frame_height - (self._size[1] // 2), self._size[1] // 2))