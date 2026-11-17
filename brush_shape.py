from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
from shape_model import ShapeModel

class BrushShape(ShapeModel):
    """
    Класс для рисования кистью

    :param path: путь QPainterPath с точками линии
    """

    def __init__(self, path, pen_color, pen_width):
        """
        Создаёт модель кисти

        :param path: путь с линией
        :param pen_color: цвет контура
        :param pen_width: толщина
        """
        rect = path.boundingRect()
        super().__init__(rect.x(), rect.y(), rect.width(), rect.height(), pen_color, "none", pen_width)
        self.path = path
        self.rotation = 0

    def draw(self, scene):
        """
        Рисует линию кисти на сцене

        :param scene: сцена QGraphicsScene
        """
        pen = QPen(QColor(self.pen_color), self.pen_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        self.item = scene.addPath(self.path, pen)

    def to_text(self):
        """
        Превращает линию кисти в строку для txt файла

        :return: строка с точками
        """
        points_str = []
        for i in range(self.path.elementCount()):
            el = self.path.elementAt(i)
            points_str.append(f"{int(el.x)},{int(el.y)}")
        points_data = ":".join(points_str)
        return f"BRUSH pen={self.pen_color} width={self.pen_width} points={points_data} rotation={self.rotation}"