import customtkinter as ctk
from figures.BaseButton import CButton

class CFigureButton(CButton):
    def __init__(self, master):
        super().__init__(master)
        self._figure = ""

    def set_figure(self, figure: str):
        self._figure = figure
        self.configure(text=self._figure, font = ("Consolas", 25))
        