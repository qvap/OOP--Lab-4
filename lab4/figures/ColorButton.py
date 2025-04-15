import customtkinter as ctk
from figures.BaseButton import CButton

class CColorButton(CButton):
    def __init__(self, master):
        super().__init__(master)
        self._button_color = "#000000"
    
    def set_color(self, color: str):
        self._button_color = color
        self.configure(fg_color = self._button_color, hover_color = self._button_color)

    def get_color(self) -> str:
        return self._button_color