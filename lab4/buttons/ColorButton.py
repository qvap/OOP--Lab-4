import customtkinter as ctk
from buttons.BaseButton import CButton

class CColorButton(CButton):
    def __init__(self, master):
        super().__init__(master)
        self._button_color = "#000000"
        self._hover_color = "#111111"
    
    def set_color(self, color: str, hover_color = str):
        self._button_color = color
        self._hover_color = hover_color
        self.configure(fg_color = self._button_color, hover_color = self._hover_color)

    def get_color(self) -> str:
        return self._button_color
    
    def get_hover_color(self) -> str:
        return self._hover_color