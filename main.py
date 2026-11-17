import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from shape_factory import ShapeFactory
from brush_shape import BrushShape
from tool_manager import ToolManager
from drawing import Drawing
from canvas_view import CanvasView


class SimpleEditor(QMainWindow):
    """
    Главное окно векторного редактора

    :ivar drawing: объект Drawing - сцена, фон и фигуры
    :ivar tool_manager: объект ToolManager - инструменты
    :ivar view: объект CanvasView - холст с размером
    :ivar pen_color: текущий цвет контура
    :ivar fill_color: текущий цвет заливки
    :ivar pen_width: текущая толщина кисти
    """

    def __init__(self):
        """
        Создаёт главное окно редактора
        """
        super().__init__()
        self.setWindowTitle("Векторный редактор")
        self.setGeometry(100, 100, 1100, 700)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.pen_color = QColor(0, 0, 0)
        self.fill_color = QColor(255, 255, 0)
        self.pen_width = 2
        self.start_point = None
        self.current_shape = None
        self.last_point = None
        self.current_path = None
        self.start_select_point = None
        self.rubber_band_item = None

        self.drawing = Drawing()
        self.tool_manager = ToolManager()
        self.view = CanvasView(self.drawing, self)

        self.view.mousePressEvent = self.mouse_press
        self.view.mouseMoveEvent = self.mouse_move
        self.view.mouseReleaseEvent = self.mouse_release

        self.create_left_panel()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_panel)
        main_layout.addWidget(self.view, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.statusBar().showMessage("Готово | Инструмент: Выбрать | Колесо мыши = зум")

    def create_left_panel(self):
        """
        Создаёт левую панель с кнопками и настройками
        """
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(220)
        layout = QVBoxLayout()
        layout.setSpacing(8)

        layout.addWidget(QLabel("<b>Фигуры</b>"))
        self.tool_group = QButtonGroup(self)

        for internal, readable in ToolManager.TOOLS:
            if internal == "fill":
                continue
            btn = QPushButton(readable)
            btn.setCheckable(True)
            btn.setProperty("tool", internal)
            btn.clicked.connect(lambda checked, t=internal: self.set_tool(t))
            self.tool_group.addButton(btn)
            layout.addWidget(btn)

            if internal == "select":
                btn.setChecked(True)

        layout.addWidget(QLabel("<br><b>Толщина кисти</b>"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 50)
        self.width_spin.setValue(2)
        self.width_spin.setSuffix(" px")
        self.width_spin.valueChanged.connect(self.change_width)
        layout.addWidget(self.width_spin)

        layout.addWidget(QLabel("<br><b>Цвета</b>"))
        self.pen_btn = QPushButton("Цвет контура")
        self.pen_btn.clicked.connect(self.choose_pen_color)
        layout.addWidget(self.pen_btn)

        self.pen_preview = QLabel()
        self.pen_preview.setFixedHeight(20)
        self.pen_preview.setStyleSheet("background-color: black; border: 1px solid gray;")
        layout.addWidget(self.pen_preview)

        self.fill_btn = QPushButton("Цвет заливки")
        self.fill_btn.clicked.connect(self.choose_fill_color)
        layout.addWidget(self.fill_btn)

        self.fill_preview = QLabel()
        self.fill_preview.setFixedHeight(20)
        self.fill_preview.setStyleSheet("background-color: yellow; border: 1px solid gray;")
        layout.addWidget(self.fill_preview)

        layout.addWidget(QLabel("<br><b>Инструменты</b>"))
        self.fill_tool_btn = QPushButton("Заливка")
        self.fill_tool_btn.setCheckable(True)
        self.fill_tool_btn.clicked.connect(lambda: self.set_tool("fill"))
        self.tool_group.addButton(self.fill_tool_btn)
        layout.addWidget(self.fill_tool_btn)

        btn_clear = QPushButton("Очистить всё")
        btn_clear.clicked.connect(self.clear_canvas)
        layout.addWidget(btn_clear)

        layout.addWidget(QLabel("<br><b>Файл</b>"))
        btn_save = QPushButton("Сохранить файл")
        btn_save.clicked.connect(self.save_project)
        layout.addWidget(btn_save)

        btn_load = QPushButton("Загрузить файл")
        btn_load.clicked.connect(self.load_project)
        layout.addWidget(btn_load)

        layout.addWidget(QLabel("<br><b>Масштаб</b>"))
        zoom_row = QHBoxLayout()
        btn_zoom_in = QPushButton("+")
        btn_zoom_in.setFixedWidth(40)
        btn_zoom_in.clicked.connect(lambda: self.view.zoom_in())
        zoom_row.addWidget(btn_zoom_in)

        btn_zoom_out = QPushButton("−")
        btn_zoom_out.setFixedWidth(40)
        btn_zoom_out.clicked.connect(lambda: self.view.zoom_out())
        zoom_row.addWidget(btn_zoom_out)

        btn_zoom_reset = QPushButton("100%")
        btn_zoom_reset.clicked.connect(lambda: self.view.zoom_reset())
        zoom_row.addWidget(btn_zoom_reset)
        layout.addLayout(zoom_row)

        self.zoom_label = QLabel("Масштаб: 100%")
        layout.addWidget(self.zoom_label)
        self.zoom_timer = QTimer()
        self.zoom_timer.timeout.connect(self.update_zoom_label)
        self.zoom_timer.start(100)

        layout.addStretch()
        self.left_panel.setLayout(layout)

    def update_zoom_label(self):
        """
        Обновляет надпись с текущим масштабом
        """
        percent = int(self.view.zoom_factor * 100)
        self.zoom_label.setText(f"Масштаб: {percent}%")

    def set_tool(self, tool):
        """
        Устанавливает текущий инструмент

        :param tool: внутреннее имя инструмента
        """
        self.tool_manager.set_tool(tool)
        readable = self.tool_manager.get_readable_name(tool)
        self.statusBar().showMessage(f"Инструмент: {readable}")

        if tool != "select":
            self.drawing.set_selection(None)

    def choose_pen_color(self):
        """
        Открывает окно выбора цвета контура.
        Если фигура выделена, то меняет цвет контура у нее
        """
        color = QColorDialog.getColor(self.pen_color, self, "Цвет контура")
        if color.isValid():
            self.pen_color = color
            self.pen_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")

            for item in self.drawing.scene.selectedItems():
                shape = self.drawing.find_shape_by_item(item)
                if shape:
                    pen = QPen(QColor(color.name()), shape.pen_width)
                    item.setPen(pen)
                    shape.pen_color = color.name()

    def choose_fill_color(self):
        """
        Открывает окно выбора цвета заливки.
        Если фигура выделена, то меняет цвет заливки у нее
        """
        color = QColorDialog.getColor(self.fill_color, self, "Цвет заливки")
        if color.isValid():
            self.fill_color = color
            self.fill_preview.setStyleSheet(f"background-color: {color.name()}; border: 1px solid gray;")

            for item in self.drawing.scene.selectedItems():
                shape = self.drawing.find_shape_by_item(item)
                if shape and not isinstance(shape, BrushShape):
                    item.setBrush(QBrush(QColor(color.name())))
                    shape.fill_color = color.name()

    def change_width(self, value):
        """
        Меняет толщину кисти

        :param value: новая толщина в пикселях
        """
        self.pen_width = value

    def mouse_press(self, event):
        """
        Обрабатывает нажатие левой кнопки мыши

        :param event: событие мыши
        """
        if event.button() != Qt.MouseButton.LeftButton: return
        pos = self.view.mapToScene(event.position().toPoint())
        if not self.drawing.scene.sceneRect().contains(pos): return

        if self.tool_manager.current_tool == "select":
            item = self.drawing.scene.itemAt(pos, self.view.transform())

            if item is None or item == self.drawing.background_rect:
                self.drawing.scene.clearSelection()
                self.start_select_point = pos
                pen = QPen(QColor(0, 120, 215), 1, Qt.PenStyle.DashLine)
                self.rubber_band_item = self.drawing.scene.addRect(
                    QRectF(pos, pos), pen, QBrush(Qt.BrushStyle.NoBrush)
                )
                self.rubber_band_item.setZValue(1000)
            else:
                QGraphicsView.mousePressEvent(self.view, event)
            return

        if self.tool_manager.current_tool == "fill":
            self.fill_at(pos)
            return

        if self.tool_manager.current_tool == "brush":
            self.last_point = pos
            self.current_path = QPainterPath()
            self.current_path.moveTo(pos)
            return

        self.start_point = pos

    def mouse_move(self, event):
        """
        Обрабатывает движение мыши для рисования кистью

        :param event: событие мыши
        """
        pos = self.view.mapToScene(event.position().toPoint())

        if self.tool_manager.current_tool == "select":
            if self.rubber_band_item is not None:
                rect = QRectF(self.start_select_point, pos).normalized()
                self.rubber_band_item.setRect(rect)
            else:
                QGraphicsView.mouseMoveEvent(self.view, event)
            return

        if not self.drawing.scene.sceneRect().contains(pos): return

        if self.tool_manager.current_tool == "brush" and self.last_point is not None:
            self.current_path.lineTo(pos)
            self.last_point = pos
            if self.current_shape:
                self.drawing.scene.removeItem(self.current_shape)
            pen = QPen(self.pen_color, self.pen_width)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            self.current_shape = self.drawing.scene.addPath(self.current_path, pen)
            return

        if self.start_point is None: return
        if self.current_shape:
            self.drawing.scene.removeItem(self.current_shape)

        x1, y1 = self.start_point.x(), self.start_point.y()
        x2, y2 = pos.x(), pos.y()
        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        pen = QPen(self.pen_color, self.pen_width)
        brush = QBrush(self.fill_color)
        tool = self.tool_manager.current_tool

        if tool == "rectangle":
            self.current_shape = self.drawing.scene.addRect(x, y, w, h, pen, brush)
        elif tool == "ellipse":
            self.current_shape = self.drawing.scene.addEllipse(x, y, w, h, pen, brush)
        elif tool == "parallelogram":
            poly = QPolygonF(
                [QPointF(x + w * 0.3, y), QPointF(x + w, y), QPointF(x + w * 0.7, y + h), QPointF(x, y + h)])
            self.current_shape = self.drawing.scene.addPolygon(poly, pen, brush)
        elif tool == "triangle":
            poly = QPolygonF([QPointF(x + w / 2, y), QPointF(x, y + h), QPointF(x + w, y + h)])
            self.current_shape = self.drawing.scene.addPolygon(poly, pen, brush)
        elif tool == "rhombus":
            poly = QPolygonF(
                [QPointF(x + w / 2, y), QPointF(x + w, y + h / 2), QPointF(x + w / 2, y + h), QPointF(x, y + h / 2)])
            self.current_shape = self.drawing.scene.addPolygon(poly, pen, brush)

    def mouse_release(self, event):
        """
        Обрабатывает отпускание мыши для фиксации фигуры

        :param event: событие мыши
        """
        if event.button() != Qt.MouseButton.LeftButton: return

        if self.tool_manager.current_tool == "select":
            if self.rubber_band_item is not None:
                rect = self.rubber_band_item.rect()
                self.drawing.scene.removeItem(self.rubber_band_item)
                self.rubber_band_item = None

                if rect.width() > 3 or rect.height() > 3:
                    items_in_rect = self.drawing.scene.items(rect)
                    for item in items_in_rect:
                        if item != self.drawing.background_rect:
                            item.setSelected(True)
                return
            else:
                QGraphicsView.mouseReleaseEvent(self.view, event)
                for shape in self.drawing.shapes:
                    if shape.item:
                        shape_rect = shape.item.sceneBoundingRect()
                        shape.x = shape_rect.x()
                        shape.y = shape_rect.y()
                        shape.w = shape_rect.width()
                        shape.h = shape_rect.height()
                return

        if self.tool_manager.current_tool == "brush":
            if self.current_shape:
                self.drawing.scene.removeItem(self.current_shape)
            shape_obj = BrushShape(self.current_path, self.pen_color.name(), self.pen_width)
            shape_obj.draw(self.drawing.scene)
            shape_obj.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
            shape_obj.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
            self.drawing.add_shape(shape_obj)
            self.current_shape = None
            self.current_path = None
            self.last_point = None
            return

        if self.current_shape:
            self.drawing.scene.removeItem(self.current_shape)
            rect = self.current_shape.boundingRect()

            shape_obj = ShapeFactory.create(
                tool=self.tool_manager.current_tool,
                x=rect.x(), y=rect.y(),
                w=rect.width(), h=rect.height(),
                pen_color=self.pen_color.name(),
                fill_color=self.fill_color.name(),
                pen_width=self.pen_width
            )

            if shape_obj:
                shape_obj.draw(self.drawing.scene)
                shape_obj.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
                shape_obj.item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
                self.drawing.add_shape(shape_obj)

        self.current_shape = None
        self.start_point = None

    def fill_at(self, pos):
        """
        Заливает фигуру или фон под курсором

        :param pos: координаты клика на сцене
        """
        items = self.drawing.scene.items(pos)
        target_item = None
        for item in items:
            if item == self.drawing.background_rect: continue
            if item == self.drawing.selection_rect: continue
            shape = self.drawing.find_shape_by_item(item)
            if shape:
                target_item = item
                break

        if target_item:
            target_item.setBrush(QBrush(self.fill_color))
            shape = self.drawing.find_shape_by_item(target_item)
            if shape:
                shape.fill_color = self.fill_color.name()
            self.statusBar().showMessage(f"Фигура залита")
        else:
            self.drawing.background_rect.setBrush(QBrush(self.fill_color))
            self.statusBar().showMessage(f"Фон залит")

    def clear_canvas(self):
        """
        Очищает холст от всех фигур
        """
        self.drawing.clear()
        self.statusBar().showMessage("Холст очищен")

    def save_project(self):
        """
        Сохраняет проект в текстовый файл
        """
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить", "проект.txt", "Text (*.txt)")
        if path:
            self.drawing.save_to_file(path)
            self.statusBar().showMessage(f"Сохранено: {path}")

    def load_project(self):
        """
        Загружает проект из текстового файла
        """
        path, _ = QFileDialog.getOpenFileName(self, "Загрузить", "", "Text (*.txt)")
        if path:
            self.drawing.load_from_file(path)
            self.statusBar().showMessage(f"Загружено: {path}")

    def keyPressEvent(self, event: QKeyEvent):
        """
        Обрабатывает нажатия клавиш на клавиатуре

        :param event: событие нажатия клавиши
        """
        if event.key() == Qt.Key.Key_Delete:
            for item in self.drawing.scene.selectedItems():
                shape = self.drawing.find_shape_by_item(item)
                if shape:
                    self.drawing.shapes.remove(shape)
                    self.drawing.scene.removeItem(item)
            event.accept()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleEditor()
    window.show()
    sys.exit(app.exec())