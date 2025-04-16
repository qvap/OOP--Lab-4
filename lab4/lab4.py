import customtkinter as ctk
from tkinter import Canvas
from math import sqrt
from figures.Circle import CCircle
from buttons.ColorButton import CColorButton
from buttons.FigureButton import CFigureButton

class Container(): # Главный контейнер объектов

    def __init__(self, canvas):
        # Private
        self.__container = list()
        self.__selected_container = list()
        self.__action = False
        self.__initial_sizes = dict()

        # Public
        self.canvas = canvas
        self.chosen_color = "#000000"
    
    def container_append(self, object: CCircle): # Добавляет в контейнер новый круг
        print(f"Appending new object: {object}")
        self.__container.append(object)
    
    def safe_move_all(self, point): # Передвигает объекты и проверяет их границы, чтобы остановить их все
        new_positions = []

        for obj in self.__selected_container:
            new_x = point.x + obj._offset_x
            new_y = point.y + obj._offset_y
            if not obj.boundaries(new_x, new_y, obj.size[0], obj.size[1], self.canvas.winfo_width(), self.canvas.winfo_height()):
                return  # Один объект не может быть перемещён — отменяем перемещение всех
            new_positions.append((obj, new_x, new_y))

        for obj, x, y in new_positions:
            obj._x = x
            obj._y = y
    
    def scale_all(self, point): # Меняет размер объектов
        new_scales = []
        weightpoint = [0, 0] # усред. точка между объектами (точка массы)
        for obj in self.__selected_container: # считаем усреднённую точку
            weightpoint[0] += obj._x
            weightpoint[1] += obj._y
        
        weightpoint = [x / len(self.__selected_container) for x in weightpoint] # среднее арифметическое

        for obj in self.__selected_container:
            new_size_coef = (self.measure_prolongate(weightpoint[0], weightpoint[1], point.x, point.y) / 100.0) + 1.0
            new_size = [x * new_size_coef for x in self.__initial_sizes[obj]]
            if not obj.boundaries(obj._x, obj._y, new_size[0], new_size[1], self.canvas.winfo_width(), self.canvas.winfo_height()):
                return
            new_scales.append((obj,new_size))
        
        for obj, new_size in new_scales:
            obj.size = new_size
        
    def measure_prolongate(self, start_point_x: int, start_point_y: int, end_point_x: int, end_point_y: int) -> float: # считает расстояние от точки до точки
        return sqrt((end_point_x - start_point_x)**2+(end_point_y - start_point_y)**2)

    def handle_mouse_click(self, point): # Создаёт новый круг и добавляет в список, если нет выделенных объектов
        if not self.__selected_container:
            self.container_append(CCircle(master=self, x=point.x, y=point.y, canvas=self.canvas))
        else:
            for object in self.__selected_container:
                object.measure_offsets(point.x, point.y)
                if self.__action:
                    self.__initial_sizes[object] = object.size

    def handle_mouse_down(self, point):
        if self.__selected_container:
            self.safe_move_all(point) if not(self.__action) else self.scale_all(point)

    def select_objects(self, point): # Выделяет круги (в зависимости от __multiple_selection меняется поведение)
        if not(self.__action):
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
    
    def initiate_additional_action(self, *args): # Включает дополнительное действие
        self.__action = True

    def stop_additional_action(self, *args): # Выключает дополнительное действие
        self.__action = False
    
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


class EditorPanel(ctk.CTkFrame): # Главная панель с кнопками
    def __init__(self, master, container):
        super().__init__(master)
        self._container = container

        self._colors = ["#FF0000", "#00FF00", "#0000FF", "#000000"]
        self._figures = ["○", "△", "▢", "▭"]

        self.configure(height=200)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1,2,3), weight=1)

        for b in range(4):
            colorbutton = CColorButton(master=self)
            colorbutton.configure(command=lambda col=self._colors[b]: self.change_color(col))
            colorbutton.set_color(self._colors[b])
            colorbutton.grid(row=0, column=b, pady=5, padx=5)

            figurebutton = CFigureButton(master=self)
            figurebutton.set_figure(self._figures[b])
            figurebutton.grid(row=1, column=b, pady=5, padx=5)
    
    def change_color(self, color: str):
        self._container.chosen_color = color


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Лабораторная работа №4")
        self.geometry("1280x720")
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(master=self, bg="#24211e", highlightbackground="#24211e")
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.container = Container(canvas=self.canvas)

        self.editorpanel = EditorPanel(master=self, container=self.container)
        self.editorpanel.grid(row=0, column=0, sticky="NW")

        self.bind("<Button-1>", self.container.handle_mouse_click)
        self.bind("<B1-Motion>", self.container.handle_mouse_down)
        self.bind("<Button-3>", self.container.select_objects)
        self.bind_all("<Escape>", self.container.deselect_objects)
        self.bind_all("<Delete>", self.container.delete_objects)
        self.bind("<KeyPress-Control_L>", self.container.initiate_additional_action)
        self.bind("<KeyRelease-Control_L>", self.container.stop_additional_action)

if __name__ == "__main__":
    app = App()
    app.mainloop()