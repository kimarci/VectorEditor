from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter, QWheelEvent, QResizeEvent
from PyQt6.QtCore import Qt

class CanvasView(QGraphicsView):
    """
    Холст с авто-подстройкой и зумом

    :ivar drawing: объект Drawing
    :ivar zoom_factor: текущий масштаб (1.0 = 100%)
    """

    def __init__(self, drawing, main_window, parent=None):
        """
        Создаёт холст

        :param drawing: объект Drawing
        :param main_window: ссылка на главное окно
        :param parent: родительский виджет
        """
        super().__init__(drawing.scene, parent)
        self.drawing = drawing
        self.main_window = main_window
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.zoom_factor = 1.0

    def resizeEvent(self, event: QResizeEvent | None):
        """
        Авто-подстройка холста под размер окна

        :param event: событие изменения размера
        """
        super().resizeEvent(event)
        rect = self.viewport().rect()
        self.scene().setSceneRect(0, 0, rect.width(), rect.height())
        self.drawing.background_rect.setRect(0, 0, rect.width(), rect.height())

    def wheelEvent(self, event: QWheelEvent | None):
        """
        Зум и поворот колесом мыши

        :param event: событие прокрутки колеса
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            angle = 5 if event.angleDelta().y() > 0 else -5
            for item in self.drawing.scene.selectedItems():
                shape = self.drawing.find_shape_by_item(item)
                if shape:
                    center = item.boundingRect().center()
                    item.setTransformOriginPoint(center)
                    shape.rotation += angle
                    item.setRotation(shape.rotation)
            return

        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        new_zoom = self.zoom_factor * factor
        if 0.1 <= new_zoom <= 10.0:
            self.scale(factor, factor)
            self.zoom_factor = new_zoom

    def zoom_in(self):
        """
        Приближение кнопкой
        """
        if self.zoom_factor < 10.0:
            self.scale(1.25, 1.25)
            self.zoom_factor *= 1.25

    def zoom_out(self):
        """
        Отдаление кнопкой
        """
        if self.zoom_factor > 0.1:
            self.scale(0.8, 0.8)
            self.zoom_factor *= 0.8

    def zoom_reset(self):
        """
        Сброс масштаба
        """
        self.resetTransform()
        self.zoom_factor = 1.0