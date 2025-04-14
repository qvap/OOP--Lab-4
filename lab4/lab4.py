import customtkinter as ctk
from tkinter import Canvas
from math import sqrt

class Figure(): # Общий класс фигуры
    def __init__(self, canvas, x, y):
        # Protected
        self._size = 1.0
        self._color ="#000000"
        self._border_color = "#ffffff"
        self._selected = False
        self._x = x
        self._y = y
        self._chosen_border_color = ""

        # Public
        self.canvas = canvas

        print(f"New point: {x}, {y}")
    
    def draw(self): # Переопред. в классе
        self._chosen_border_color = self._border_color if self._selected else self._color

    def select(self):
        self._selected = True

    def deselect(self):
        self._selected = False
    
    def mousecheck(self, x: int, y: int): # Переопред. в классе
        pass

    def destroy(self) -> bool:
        if self._selected:
            del self
            return True
        return False

class CCircle(Figure): # Базовый класс круга

    def __init__(self, canvas, x, y):
        super().__init__(canvas=canvas, x=x, y=y)

        # Private
        self._radius = 50

    def draw(self): # Отрисовывает круг на Canvas
        super().draw()
        self.canvas.create_oval(self._x - self._radius, self._y - self._radius,\
            self._x + self._radius, self._y + self._radius, fill = self._color, width = 5, outline = self._chosen_border_color)

    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри круга
        return ((x - self._x)**2 + (y - self._y)**2) <= self._radius**2

class Container():

    def __init__(self, canvas):
        # Private
        self.__container = list()
        self.__selected_container = list()
        self.__multiple_selection = False

        # Public
        self.canvas = canvas
    
    def container_append(self, object: CCircle): # Добавляет в контейнер новый круг
        print(f"Appending new object: {object}")
        self.__container.append(object)
    
    def create_objects(self, point): # Создаёт новый круг и добавляет в список
        self.container_append(CCircle(x=point.x, y=point.y, canvas=self.canvas))
    
    def select_objects(self, point): # Выделяет круги (в зависимости от __multiple_selection меняется поведение)
        if not(self.__multiple_selection):
            for circle in self.__selected_container:
                circle.deselect()
            self.__selected_container.clear()
        
        self.__selected_container.extend(list(filter(lambda x: x.mousecheck(point.x, point.y), self.__container)))
        for circle in self.__selected_container:
            circle.select()
    
    def deselect_objects(self, *args): # Снимает выделение со всех кругов
        for circle in self.__selected_container:
            circle.deselect()
        self.__selected_container.clear()
    
    def delete_objects(self, *args): # Удаляет выделенные объекты
        self.__container = [obj for obj in self.__container if not obj.destroy()]
        self.__selected_container.clear()
    
    def initiate_selection(self, *args): # Включает множественное выделение
        self.__multiple_selection = True

    def stop_selection(self, *args): # Выключает множественное выделение
        self.__multiple_selection = False
    
    def __getattribute__(self, name): # событие Paint
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self.canvas.delete("all")
                for circle in self.__container:
                    circle.draw()
                return result
            return wrapper
        return attr

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Лабораторная работа №3")
        self.geometry("400x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(master=self, bg="#24211e", highlightbackground="#24211e")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.container = Container(canvas=self.canvas)

        self.bind("<Button-1>", self.container.create_objects)
        self.bind("<Button-3>", self.container.select_objects)
        self.bind_all("<Escape>", self.container.deselect_objects)
        self.bind_all("<Delete>", self.container.delete_objects)
        self.bind("<KeyPress-Control_L>", self.container.initiate_selection)
        self.bind("<KeyRelease-Control_L>", self.container.stop_selection)

if __name__ == "__main__":
    app = App()
    app.mainloop()