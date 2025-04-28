from math import sqrt

class Tools(): # Класс со вспомогательными функциями
    @staticmethod
    def measure_prolongate(start_point_x: int, start_point_y: int, end_point_x: int, end_point_y: int) -> float: # считает расстояние от точки до точки
        return sqrt((end_point_x - start_point_x)**2+(end_point_y - start_point_y)**2)
    
    @staticmethod
    def clamp(value: float, up_limit: float, low_limit: float) -> float: # Содержит значение в границах
        if value < low_limit:
            return low_limit
        elif value > up_limit:
            return up_limit
        return value