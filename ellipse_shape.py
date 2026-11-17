from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt
from shape_model import ShapeModel

class EllipseShape(ShapeModel):
    """
    Класс для рисования овала
    """

    def draw(self, scene):
        """
        Рисует овал на сцене

        :param scene: сцена QGraphicsScene
        """
        pen = QPen(QColor(self.pen_color), self.pen_width)
        brush = QBrush(QColor(self.fill_color)) if self.fill_color != "none" else Qt.BrushStyle.NoBrush
        self.item = scene.addEllipse(self.x, self.y, self.w, self.h, pen, brush)