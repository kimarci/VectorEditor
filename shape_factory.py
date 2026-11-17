from rectangle_shape import RectangleShape
from ellipse_shape import EllipseShape
from parallelogram_shape import ParallelogramShape
from triangle_shape import TriangleShape
from rhombus_shape import RhombusShape
from brush_shape import BrushShape


class ShapeFactory:
    """
    Создает объект по имени.
    """

    @staticmethod
    def create(tool, x, y, w, h, pen_color, fill_color, pen_width):
        """
        Создаёт объект фигуры по внутреннему имени инструмента.

        :param tool: внутреннее имя (rectangle, ellipse и т.д.)
        :param x: координата X
        :param y: координата Y
        :param w: ширина
        :param h: высота
        :param pen_color: цвет контура
        :param fill_color: цвет заливки
        :param pen_width: толщина
        :return: объект фигуры или None
        """
        if tool == "rectangle":
            return RectangleShape(x, y, w, h, pen_color, fill_color, pen_width)
        elif tool == "ellipse":
            return EllipseShape(x, y, w, h, pen_color, fill_color, pen_width)
        elif tool == "parallelogram":
            return ParallelogramShape(x, y, w, h, pen_color, fill_color, pen_width)
        elif tool == "triangle":
            return TriangleShape(x, y, w, h, pen_color, fill_color, pen_width)
        elif tool == "rhombus":
            return RhombusShape(x, y, w, h, pen_color, fill_color, pen_width)
        return None