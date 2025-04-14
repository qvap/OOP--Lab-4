import customtkinter as ctk
from tkinter import Canvas
from math import sqrt
from figures.Circle import CCircle

class Container():

    def __init__(self, canvas):
        # Private
        self.__container = list()
        self.__selected_container = list()
        self.__multiple_selection = False

        # Public
        self.canvas = canvas
        self.should_stop = False # если один объект застрял
    
    def container_append(self, object: CCircle): # Добавляет в контейнер новый круг
        print(f"Appending new object: {object}")
        self.__container.append(object)
    
    def handle_mouse_click(self, point): # Создаёт новый круг и добавляет в список, если нет выделенных объектов
        if not self.__selected_container:
            self.container_append(CCircle(x=point.x, y=point.y, canvas=self.canvas))
        else:
            for object in self.__selected_container:
                object.measure_offsets(point.x, point.y)

    def safe_move_all(self, point): # Передвигает объекты и проверяет их границы, чтобы остановить их все
        new_positions = []

        for obj in self.__selected_container:
            new_x = point.x + obj._offset_x
            new_y = point.y + obj._offset_y

            if not obj.boundaries(new_x, new_y, self.canvas.winfo_width(), self.canvas.winfo_height()):
                return  # Один объект не может быть перемещён — отменяем перемещение всех

            new_positions.append((obj, new_x, new_y))

        for obj, x, y in new_positions:
            obj._x = x
            obj._y = y

    def get_movement_status(self) -> bool:
        return self.should_stop

    def handle_mouse_down(self, point):
        if self.__selected_container:
            self.safe_move_all(point)

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

        self.bind("<Button-1>", self.container.handle_mouse_click)
        self.bind("<B1-Motion>", self.container.handle_mouse_down)
        self.bind("<Button-3>", self.container.select_objects)
        self.bind_all("<Escape>", self.container.deselect_objects)
        self.bind_all("<Delete>", self.container.delete_objects)
        self.bind("<KeyPress-Control_L>", self.container.initiate_selection)
        self.bind("<KeyRelease-Control_L>", self.container.stop_selection)

if __name__ == "__main__":
    app = App()
    app.mainloop()