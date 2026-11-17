class ShapeModel:
    """
    Модель данных одной фигуры

    :param x: координата X левого верхнего угла
    :param y: координата Y левого верхнего угла
    :param w: ширина фигуры
    :param h: высота фигуры
    :param pen_color: цвет контура
    :param fill_color: цвет заливки
    :param pen_width: толщина контура
    """

    def __init__(self, x, y, w, h, pen_color, fill_color, pen_width):
        """
        Создаёт модель фигуры

        :param x: координата X
        :param y: координата Y
        :param w: ширина
        :param h: высота
        :param pen_color: цвет контура
        :param fill_color: цвет заливки
        :param pen_width: толщина контура
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pen_color = pen_color
        self.fill_color = fill_color
        self.pen_width = pen_width
        self.item = None
        self.rotation = 0

    def draw(self, scene):
        """
        Рисует фигуру на сцене

        :param scene: сцена QGraphicsScene
        """
        pass

    def to_text(self):
        """
        Превращает фигуру в строку для сохранения в txt-файл

        :return: строка с данными фигуры
        """
        fill = self.fill_color if self.fill_color else "none"
        shape_type = self.__class__.__name__.upper()
        return f"{shape_type} x={self.x} y={self.y} w={self.w} h={self.h} pen={self.pen_color} fill={fill} width={self.pen_width} rotation={self.rotation}"