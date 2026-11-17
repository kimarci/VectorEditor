from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from shape_model import ShapeModel

class RectangleShape(ShapeModel):
    """
    Класс для рисования прямоугольника
    """

    def draw(self, scene):
        """
        Рисует прямоугольник на сцене

        :param scene: сцена QGraphicsScene
        """
        pen = QPen(QColor(self.pen_color), self.pen_width)
        brush = QBrush(QColor(self.fill_color)) if self.fill_color != "none" else Qt.BrushStyle.NoBrush
        self.item = scene.addRect(self.x, self.y, self.w, self.h, pen, brush)