from PyQt6.QtWidgets import QGraphicsScene, QGraphicsItem
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF

from rectangle_shape import RectangleShape
from ellipse_shape import EllipseShape
from parallelogram_shape import ParallelogramShape
from triangle_shape import TriangleShape
from rhombus_shape import RhombusShape
from brush_shape import BrushShape

class Drawing:
    """
    Рисунок, который хранит сцену, фон и фигуры

    :ivar scene: сцена QGraphicsScene, где лежат все объекты
    :ivar background_rect: фоновый прямоугольник
    :ivar shapes: список моделей фигур
    :ivar selection_rect:  рамка выделения объектов
    """

    def __init__(self, width=800, height=650):
        """
        Создаёт холст

        :param width: ширина холста в пикселях
        :param height: высота холста в пикселях
        """
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, width, height)

        self.background_rect = self.scene.addRect(
            0, 0, width, height,
            QPen(Qt.PenStyle.NoPen),
            QBrush(QColor(255, 255, 255))
        )
        self.background_rect.setZValue(-1000)

        self.shapes = []
        self.selected_shape = None

        # Создаём рамку выделения
        pen = QPen(QColor(0, 120, 215), 2, Qt.PenStyle.DashLine)
        self.selection_rect = self.scene.addRect(
            QRectF(0, 0, 0, 0),
            pen,
            QBrush(Qt.BrushStyle.NoBrush)
        )
        self.selection_rect.setZValue(1000)
        self.selection_rect.setVisible(False)
        self.selection_rect.setAcceptedMouseButtons(Qt.MouseButton.NoButton)

    def add_shape(self, shape_model):
        """
        Добавляет фигуру в список

        :param shape_model: модель фигуры
        """
        self.shapes.append(shape_model)

    def clear(self):
        """
        Удаляет все фигуры, фон становится белым
        """
        for shape in self.shapes:
            if shape.item:
                self.scene.removeItem(shape.item)
        self.shapes.clear()
        self.selected_shape = None
        self.background_rect.setBrush(QBrush(QColor(255, 255, 255)))
        self.selection_rect.setVisible(False)

    def find_shape_by_item(self, item):
        """
        Поиск фигуры по графическому объекту

        :param item: графический объект
        :return: модель фигуры или None
        """
        for shape in self.shapes:
            if shape.item == item:
                return shape
        return None

    def set_selection(self, shape_model):
        """
        Показывает рамку вокруг фигуры или убирает её

        :param shape_model: модель фигуры
        """
        self.selected_shape = shape_model
        if shape_model:
            self.selection_rect.setRect(
                QRectF(
                    shape_model.x - 3,
                    shape_model.y - 3,
                    shape_model.w + 6,
                    shape_model.h + 6
                )
            )
            self.selection_rect.setVisible(True)
        else:
            self.selection_rect.setVisible(False)

    def save_to_file(self, path):
        """
        Сохраняет все фигуры в текстовый файл

        :param path: путь к файлу
        """
        with open(path, "w", encoding="utf-8") as f:
            bg_color = self.background_rect.brush().color().name()
            f.write(f"BACKGROUND {bg_color}\n")
            for shape in self.shapes:
                f.write(shape.to_text() + "\n")

    def load_from_file(self, path):
        """
        Загружает фигуры из текстового файла

        :param path: путь к файлу
        """
        self.clear()
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ")
            shape_type = parts[0]

            if shape_type == "BACKGROUND":
                bg_color = parts[1]
                self.background_rect.setBrush(QBrush(QColor(bg_color)))
                continue

            params = {}
            for part in parts[1:]:
                key, value = part.split("=")
                params[key] = value

            shape = None
            if shape_type == "RECTANGLESHAPE":
                shape = RectangleShape(float(params["x"]), float(params["y"]), float(params["w"]), float(params["h"]), params["pen"], params["fill"], int(params["width"]))
            elif shape_type == "ELLIPSESHAPE":
                shape = EllipseShape(float(params["x"]), float(params["y"]), float(params["w"]), float(params["h"]), params["pen"], params["fill"], int(params["width"]))
            elif shape_type == "PARALLELOGRAMSHAPE":
                shape = ParallelogramShape(float(params["x"]), float(params["y"]), float(params["w"]), float(params["h"]), params["pen"], params["fill"], int(params["width"]))
            elif shape_type == "TRIANGLESHAPE":
                shape = TriangleShape(float(params["x"]), float(params["y"]), float(params["w"]), float(params["h"]), params["pen"], params["fill"], int(params["width"]))
            elif shape_type == "RHOMBUSSHAPE":
                shape = RhombusShape(float(params["x"]), float(params["y"]), float(params["w"]), float(params["h"]), params["pen"], params["fill"], int(params["width"]))
            elif shape_type == "BRUSH":
                path_obj = QPainterPath()
                pts = params["points"].split(":")
                for i, p in enumerate(pts):
                    px, py = map(float, p.split(","))
                    if i == 0:
                        path_obj.moveTo(px, py)
                    else:
                        path_obj.lineTo(px, py)
                shape = BrushShape(path_obj, params["pen"], int(params["width"]))

            if shape:
                shape.draw(self.scene)
                if shape.item:
                    shape.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
                    shape.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
                if "rotation" in params:
                    shape.rotation = int(params["rotation"])
                    center = shape.item.boundingRect().center()
                    shape.item.setTransformOriginPoint(center)
                    shape.item.setRotation(shape.rotation)
                self.shapes.append(shape)