import customtkinter as ctk
from tkinter import Canvas
from Tools import Tools
from figures.Circle import CCircle
from figures.Rectangle import CRectangle
from figures.Square import CSquare
from figures.Triangle import CTriangle
from buttons.ColorButton import CColorButton
from buttons.FigureButton import CFigureButton

class Container(): # Главный контейнер объектов

    def __init__(self, master, canvas):
        # Private
        self.__container = list()
        self.__selected_container = list()
        self.__action = False
        self.__initial_sizes = dict()
        self.__app = master

        # Public
        self.canvas = canvas
        self.chosen_color = "#000000"
        self.chosen_figure = "○"

    def safe_move_all(self, point): # Передвигает объекты и проверяет их границы, чтобы остановить их все
        new_positions = []

        for obj in self.__selected_container:
            obj_size = obj.pass_size()
            new_x = point.x + obj._offset_x
            new_y = point.y + obj._offset_y
            if not obj.boundaries(new_x, new_y, obj_size[0], obj_size[1], self.canvas.winfo_width(), self.canvas.winfo_height()):
                return  # Один объект не может быть перемещён — отменяем перемещение всех
            new_positions.append((obj, new_x, new_y))

        for obj, x, y in new_positions:
            obj.move(x, y)
    
    def scale_all(self, point): # Меняет размер объектов
        new_scales = []
        weightpoint = [0, 0] # усред. точка между объектами (точка массы)
        for obj in self.__selected_container: # считаем усреднённую точку
            obj_coords = obj.pass_coordinates()
            weightpoint[0] += obj_coords[0]
            weightpoint[1] += obj_coords[1]
        
        weightpoint = [x / len(self.__selected_container) for x in weightpoint] # среднее арифметическое

        for obj in self.__selected_container:
            obj_coords = obj.pass_coordinates()
            new_size_coef = (Tools.measure_prolongate(weightpoint[0], weightpoint[1], point.x, point.y) / 100.0) + 1.0
            new_size = [x * new_size_coef for x in self.__initial_sizes[obj]]
            if not obj.boundaries(obj_coords[0], obj_coords[1], new_size[0], new_size[1], self.canvas.winfo_width(), self.canvas.winfo_height()):
                return
            new_scales.append((obj,new_size))
        
        for obj, new_size in new_scales:
            obj.resize(new_size)

    def handle_mouse_click(self, point): # Что происходит во время нажатия мышью
        __widget = self.__app.winfo_containing(point.x_root, point.y_root)
        if __widget == self.canvas:
            if not self.__selected_container:
                self.create_object(point.x, point.y)
            else:
                for object in self.__selected_container:
                    object.measure_offsets(point.x, point.y)
        
    def handle_mouse_down(self, point): # Что происходит во время зажатия мышью
        __widget = self.__app.winfo_containing(point.x_root, point.y_root)
        if self.__selected_container and __widget == self.canvas:
            self.safe_move_all(point) if not(self.__action) else self.scale_all(point)

            self.redraw()
    
    def create_object(self, x: int, y: int): # Создаёт новый объект по координатам
        figure_classes = {
            "○": CCircle,
            "▢": CSquare,
            "▭": CRectangle,
            "△": CTriangle
        }
        figure_class = figure_classes.get(self.chosen_figure)
        if figure_class:
            obj = figure_class(master=self, x=x, y=y, canvas=self.canvas)
            self.container_append(obj)
            obj.check_outside()
        else:
            raise TypeError("Such figure class is not presented")

        self.redraw()
            
    def container_append(self, object): # Добавляет в контейнер новую фигуру
        print(f"Appending new object: {object}")
        self.__container.insert(0, object)
        self.__initial_sizes[object] = object.pass_size()
    
    def select_objects(self, point): # Выделяет круги
        self.deselect_objects()
        
        for figure in self.__container:
            if figure.mousecheck(point.x, point.y):
                self.__selected_container.insert(0, figure)
                if not(self.__action):
                    break
        
        self.redraw()
    
    def deselect_objects(self, *args): # Снимает выделение со всех кругов
        if not(self.__action):
            self.__selected_container.clear()
    
    def delete_objects(self, *args): # Удаляет выделенные объекты
        for obj in self.__selected_container:
            if obj in self.__container:
                self.__container.remove(obj)
            else:
                raise IndexError("No such object in main container")
            del obj
        self.__selected_container.clear()

        self.redraw()
    
    def initiate_additional_action(self, *args): # Включает дополнительное действие
        self.__action = True

    def stop_additional_action(self, *args): # Выключает дополнительное действие
        self.__action = False
    
    def redraw(self):
        self.canvas.delete("all")
        for figure_index in range(len(self.__container) - 1, -1, -1):
            draw_border = True if self.__container[figure_index] in self.__selected_container else False
            self.__container[figure_index].draw(draw_border)


class EditorPanel(ctk.CTkFrame): # Главная панель с кнопками
    def __init__(self, master, container):
        super().__init__(master)
        self._container = container

        colors = ["#FF0000", "#00FF00", "#0000FF", "#000000"]
        hover_colors = ["#AA0000", "#00AA00", "#0000AA", "#444444"]
        figures = ["○", "△", "▢", "▭"]

        self.configure(height=200)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1,2,3), weight=1)

        for b in range(4):
            colorbutton = CColorButton(master=self)
            colorbutton.configure(command=lambda col=colors[b]: self.change_color(col))
            colorbutton.set_color(colors[b], hover_colors[b])
            colorbutton.grid(row=0, column=b, pady=5, padx=5)

            figurebutton = CFigureButton(master=self)
            figurebutton.configure(command=lambda figure=figures[b]: self.change_figure(figure))
            figurebutton.set_figure(figures[b])
            figurebutton.grid(row=1, column=b, pady=5, padx=5)
    
    def change_color(self, color: str):
        self._container.chosen_color = color
    
    def change_figure(self, figure: str):
        self._container.chosen_figure = figure

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

        self.container = Container(canvas=self.canvas, master=self)

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