from PyQt6.QtGui import QPen, QBrush, QColor, QPolygonF
from PyQt6.QtCore import Qt, QPointF
from shape_model import ShapeModel

class TriangleShape(ShapeModel):
    """
    Класс для рисования треугольника
    """

    def draw(self, scene):
        """
        Рисует треугольник на сцене

        :param scene: сцена QGraphicsScene
        """
        pen = QPen(QColor(self.pen_color), self.pen_width)
        brush = QBrush(QColor(self.fill_color)) if self.fill_color != "none" else Qt.BrushStyle.NoBrush
        polygon = QPolygonF([
            QPointF(self.x + self.w / 2, self.y),
            QPointF(self.x, self.y + self.h),
            QPointF(self.x + self.w, self.y + self.h)
        ])
        self.item = scene.addPolygon(polygon, pen, brush)