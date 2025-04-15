import customtkinter as ctk

class CButton(ctk.CTkButton): # кнопка в панели
    def __init__(self, master):
        super().__init__(master)
        self.configure(width=50, height=50, text="")