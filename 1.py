import sys
import json
from itertools import permutations
from typing import Optional, List, Dict, Set

from PySide6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                               QGraphicsItem, QGraphicsEllipseItem,
                               QGraphicsLineItem, QGraphicsTextItem,
                               QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QPushButton, QFileDialog, QMessageBox, QLabel, 
                               QScrollArea, QGroupBox, QFrame, QSizePolicy)
from PySide6.QtCore import Qt, QRectF, QLineF, QPointF, Signal, QObject, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPen, QBrush, QColor, QPainter, QPainterPathStroker, QAction, QFont, QLinearGradient


# ==========================================
# 1. Configuration (Конфигурация)
# ==========================================
class GraphConfig:
    NODE_DIAMETER = 42
    NODE_RADIUS = NODE_DIAMETER / 2
    EDGE_WIDTH = 3
    MIN_DISTANCE = 50

    # Light theme colors
    COLOR_BG = QColor(248, 250, 252)
    COLOR_NODE = QColor(41, 128, 185)  # Blue
    COLOR_NODE_ACTIVE = QColor(231, 76, 60)  # Red
    COLOR_EDGE = QColor(149, 165, 166)  # Gray
    COLOR_TEXT = QColor(44, 62, 80)  # Dark blue-gray
    
    COLOR_SUCCESS = QColor(46, 204, 113)  # Green
    COLOR_WARNING = QColor(241, 196, 15)  # Yellow
    COLOR_ERROR = QColor(231, 76, 60)  # Red
    
    TABLE_BG = QColor(255, 255, 255)
    TABLE_HEADER = QColor(245, 247, 250)
    TABLE_TEXT = QColor(44, 62, 80)
    TABLE_DIAGONAL = QColor(240, 242, 245)
    TABLE_BORDER = QColor(220, 223, 228)


# ==========================================
# 2. Custom Widgets (Кастомные виджеты)
# ==========================================
class MaterialButton(QPushButton):
    def __init__(self, text, color="#3498db", icon=None):
        super().__init__(text)
        self.color = QColor(color)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        
        style = f"""
            QPushButton {{
                background-color: {self.color.name()};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.color.darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {self.color.darker(130).name()};
                padding: 9px 19px 7px 21px;
            }}
        """
        self.setStyleSheet(style)


class MaterialTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 8px;
                border: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
        """)
        self.setAlternatingRowColors(True)
        
        font = QFont("Segoe UI", 10)
        self.setFont(font)


# ==========================================
# 3. Graph Visual Entities (Виджеты Графа)
# ==========================================
class EdgeItem(QGraphicsLineItem):
    def __init__(self, source_item, dest_item):
        super().__init__()
        self.source = source_item
        self.dest = dest_item
        self.setPen(QPen(GraphConfig.COLOR_EDGE, GraphConfig.EDGE_WIDTH, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        self.setZValue(0)
        self.update_geometry()

    def update_geometry(self):
        line = QLineF(self.source.scenePos(), self.dest.scenePos())
        self.setLine(line)

    def shape(self):
        path = super().shape()
        stroker = QPainterPathStroker()
        stroker.setWidth(12)
        return stroker.createStroke(path)


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, name: str, x: float, y: float):
        rect = QRectF(-GraphConfig.NODE_RADIUS, -GraphConfig.NODE_RADIUS,
                      GraphConfig.NODE_DIAMETER, GraphConfig.NODE_DIAMETER)
        super().__init__(rect)
        self.name = name
        self.edges: List[EdgeItem] = []
        
        # Create gradient for node
        gradient = QLinearGradient(-GraphConfig.NODE_RADIUS, -GraphConfig.NODE_RADIUS,
                                  GraphConfig.NODE_DIAMETER, GraphConfig.NODE_DIAMETER)
        gradient.setColorAt(0, GraphConfig.COLOR_NODE.lighter(120))
        gradient.setColorAt(1, GraphConfig.COLOR_NODE)
        self.setBrush(QBrush(gradient))
        
        self.setPen(QPen(GraphConfig.COLOR_NODE.darker(130), 2))
        self.setPos(x, y)
        self.setZValue(2)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self._create_label(name)

    def _create_label(self, text: str):
        self.label = QGraphicsTextItem(text, self)
        self.label.setDefaultTextColor(Qt.GlobalColor.white)
        font = QFont("Segoe UI", 11, QFont.Weight.Bold)
        self.label.setFont(font)
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, -rect.height() / 2)

    def hoverEnterEvent(self, event):
        self.setPen(QPen(QColor(255, 255, 255), 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(GraphConfig.COLOR_NODE.darker(130), 2))
        super().hoverLeaveEvent(event)

    def set_highlighted(self, is_active: bool):
        if is_active:
            gradient = QLinearGradient(-GraphConfig.NODE_RADIUS, -GraphConfig.NODE_RADIUS,
                                      GraphConfig.NODE_DIAMETER, GraphConfig.NODE_DIAMETER)
            gradient.setColorAt(0, GraphConfig.COLOR_NODE_ACTIVE.lighter(120))
            gradient.setColorAt(1, GraphConfig.COLOR_NODE_ACTIVE)
            self.setBrush(QBrush(gradient))
            self.setPen(QPen(GraphConfig.COLOR_NODE_ACTIVE.darker(130), 3))
        else:
            gradient = QLinearGradient(-GraphConfig.NODE_RADIUS, -GraphConfig.NODE_RADIUS,
                                      GraphConfig.NODE_DIAMETER, GraphConfig.NODE_DIAMETER)
            gradient.setColorAt(0, GraphConfig.COLOR_NODE.lighter(120))
            gradient.setColorAt(1, GraphConfig.COLOR_NODE)
            self.setBrush(QBrush(gradient))
            self.setPen(QPen(GraphConfig.COLOR_NODE.darker(130), 2))

    def add_connection(self, edge: EdgeItem):
        self.edges.append(edge)

    def remove_connection(self, edge: EdgeItem):
        if edge in self.edges:
            self.edges.remove(edge)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged and self.scene():
            for edge in self.edges:
                edge.update_geometry()
        return super().itemChange(change, value)


# ==========================================
# 4. Graph Logic Managers
# ==========================================
class ChainBuilder:
    def __init__(self):
        self.active_node: Optional[NodeItem] = None

    def start_or_continue(self, node: NodeItem) -> Optional[NodeItem]:
        prev_node = self.active_node
        if self.active_node:
            self.active_node.set_highlighted(False)
        self.active_node = node
        self.active_node.set_highlighted(True)
        return prev_node

    def reset(self):
        if self.active_node:
            self.active_node.set_highlighted(False)
            self.active_node = None


class GraphManager(QObject):
    node_count_changed = Signal(int)

    def __init__(self, scene: QGraphicsScene):
        super().__init__()
        self.scene = scene
        self.node_counter = 0

    def reset(self):
        self.node_counter = 0
        self.scene.clear()
        self.node_count_changed.emit(0)

    def generate_name(self) -> str:
        n = self.node_counter
        name = ""
        while n >= 0:
            name = chr(ord('A') + (n % 26)) + name
            n = n // 26 - 1
        self.node_counter += 1
        return name

    def create_node(self, pos: QPointF, name: str = None) -> NodeItem:
        if name is None:
            name = self.generate_name()
        else:
            self.node_counter += 1

        node = NodeItem(name, pos.x(), pos.y())
        self.scene.addItem(node)
        self.node_count_changed.emit(self.get_node_count())
        return node

    def create_edge(self, u: NodeItem, v: NodeItem):
        if u == v: return
        for edge in u.edges:
            if (edge.source == u and edge.dest == v) or (edge.source == v and edge.dest == u):
                return
        edge = EdgeItem(u, v)
        self.scene.addItem(edge)
        u.add_connection(edge)
        v.add_connection(edge)

    def delete_item(self, item: QGraphicsItem):
        if isinstance(item, NodeItem):
            for edge in list(item.edges):
                self.delete_item(edge)
            self.scene.removeItem(item)
            self.node_count_changed.emit(self.get_node_count())
        elif isinstance(item, EdgeItem):
            item.source.remove_connection(item)
            item.dest.remove_connection(item)
            self.scene.removeItem(item)

    def get_node_count(self) -> int:
        return sum(1 for item in self.scene.items() if isinstance(item, NodeItem))

    def is_position_valid(self, pos: QPointF) -> bool:
        for item in self.scene.items():
            if isinstance(item, NodeItem):
                distance = QLineF(pos, item.scenePos()).length()
                if distance < GraphConfig.MIN_DISTANCE:
                    return False
        return True

    def get_graph_structure(self) -> Dict[str, Set[str]]:
        structure = {}
        nodes = [item for item in self.scene.items() if isinstance(item, NodeItem)]
        for node in nodes:
            structure[node.name] = set()

        for node in nodes:
            for edge in node.edges:
                other = edge.dest if edge.source == node else edge.source
                structure[node.name].add(other.name)
        
        return structure


# ==========================================
# 5. Matrix Widget (Таблица весов)
# ==========================================
class WeightMatrixWidget(MaterialTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(0)
        self.setRowCount(0)
        self.setWindowTitle("Матрица весов")

        self.horizontalHeader().setDefaultSectionSize(45)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.itemChanged.connect(self.on_item_changed)

    def update_size(self, node_count: int):
        self.setRowCount(node_count)
        self.setColumnCount(node_count)

        headers = [str(i + 1) for i in range(node_count)]
        self.setHorizontalHeaderLabels(headers)
        self.setVerticalHeaderLabels(headers)

        self.blockSignals(True)
        for r in range(node_count):
            for c in range(node_count):
                item = self.item(r, c)
                if not item:
                    item = QTableWidgetItem("")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(r, c, item)

                if r == c:
                    item.setFlags(Qt.ItemIsEnabled)
                    item.setBackground(QBrush(GraphConfig.TABLE_DIAGONAL))
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                    item.setBackground(QBrush(GraphConfig.TABLE_BG))
        self.blockSignals(False)

    def on_item_changed(self, item):
        row = item.row()
        col = item.column()
        if row == col: return

        text = item.text()
        self.blockSignals(True)
        symmetric_item = self.item(col, row)
        if symmetric_item:
            symmetric_item.setText(text)
        self.blockSignals(False)

    def get_data(self) -> List[List[str]]:
        rows = self.rowCount()
        data = []
        for r in range(rows):
            row_data = []
            for c in range(rows):
                item = self.item(r, c)
                row_data.append(item.text() if item else "")
            data.append(row_data)
        return data

    def set_data(self, data: List[List[str]]):
        size = len(data)
        self.update_size(size)
        self.blockSignals(True)
        for r in range(size):
            for c in range(size):
                if r < len(data) and c < len(data[r]):
                    val = data[r][c]
                    item = self.item(r, c)
                    if item:
                        item.setText(val)
        self.blockSignals(False)

    def get_structure(self) -> Dict[str, Set[str]]:
        structure = {}
        rows = self.rowCount()
        headers = [str(i + 1) for i in range(rows)]
        
        for r in range(rows):
            node_idx = headers[r]
            neighbors = set()
            for c in range(rows):
                if r == c: continue
                item = self.item(r, c)
                if item and item.text().strip() and item.text().strip() != '0':
                    neighbors.add(headers[c])
            structure[node_idx] = neighbors
        
        return structure


# ==========================================
# 6. Graph Scene
# ==========================================
class GraphScene(QGraphicsScene):
    def __init__(self, manager: GraphManager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.chain_builder = ChainBuilder()
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0, QColor(248, 250, 252))
        gradient.setColorAt(1, QColor(240, 242, 245))
        self.setBackgroundBrush(QBrush(gradient))
        
        self.setSceneRect(0, 0, 800, 600)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.chain_builder.reset()
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        pos = event.scenePos()
        item = self.itemAt(pos, self.views()[0].transform())

        if event.button() == Qt.LeftButton:
            # Режим создания связей (Shift + Click)
            if event.modifiers() & Qt.ShiftModifier:
                if isinstance(item, NodeItem):
                    prev_node = self.chain_builder.start_or_continue(item)
                    if prev_node:
                        self.manager.create_edge(prev_node, item)
                    event.accept()
                    return
                else:
                    self.chain_builder.reset()
            else:
                self.chain_builder.reset()

            # Создание узла
            if item is None:
                if self.manager.is_position_valid(pos):
                    self.manager.create_node(pos)
                event.accept()
                return

            super().mousePressEvent(event)

        elif event.button() == Qt.RightButton:
            # Удаление
            self.chain_builder.reset()
            if item:
                self.manager.delete_item(item)
                event.accept()


class GraphSolver:
    @staticmethod
    def solve(graph_structure: Dict[str, Set[str]], matrix_structure: Dict[str, Set[str]]) -> List[Dict[str, str]]:
        graph_nodes = sorted(list(graph_structure.keys()))
        table_nodes = sorted(list(matrix_structure.keys()))
        
        n = len(graph_nodes)
        m = len(table_nodes)
        
        if n == 0 or m == 0:
            return []
        
        if n != m:
            return []

        solutions = []

        for p in permutations(graph_nodes):
            mapping = {t_node: g_node for t_node, g_node in zip(table_nodes, p)}
            transformed_matrix = {}

            for t_node, neighbors in matrix_structure.items():
                mapped_node = mapping[t_node]
                mapped_neighbors = {mapping[n] for n in neighbors}
                transformed_matrix[mapped_node] = mapped_neighbors
            
            if transformed_matrix == graph_structure:
                solutions.append(mapping)

        return solutions


# ==========================================
# 7. Main Application Window
# ==========================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Тренажер: Изоморфизм графов (ЕГЭ Информатика)")
        self.resize(1300, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
            }
        """)

        # 1. Инициализация
        self.scene_dummy = QGraphicsScene()
        self.graph_manager = GraphManager(self.scene_dummy)
        self.scene = GraphScene(self.graph_manager, self)
        self.graph_manager.scene = self.scene

        # 2. Создание виджетов
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setStyleSheet("border: 2px solid #e0e0e0; border-radius: 10px; background-color: white;")
        
        self.matrix_widget = WeightMatrixWidget()
        
        # Создание кнопок с иконками
        self.solve_button = MaterialButton("🔍 Найти соответствие", "#9b59b6")
        self.solve_button.clicked.connect(self.solve_graph)
        
        self.clear_button = MaterialButton("🗑️ Очистить всё", "#95a5a6")
        self.clear_button.clicked.connect(self.clear_all)
        
        self.save_button = MaterialButton("💾 Сохранить", "#3498db")
        self.save_button.clicked.connect(self.save_exercise)
        
        self.load_button = MaterialButton("📂 Загрузить", "#2ecc71")
        self.load_button.clicked.connect(self.load_exercise)
        
        # Результаты
        result_frame = QFrame()
        result_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        self.result_label = QLabel("�� Нарисуйте граф справа и заполните матрицу весов слева, затем нажмите 'Найти соответствие'")
        self.result_label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        self.result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.result_label.setWordWrap(True)
        
        result_layout = QVBoxLayout(result_frame)
        result_layout.addWidget(QLabel("<b style='color: #2c3e50; font-size: 16px;'>Результат:</b>"))
        result_layout.addWidget(self.result_label)
        
        # Скролл для результатов
        scroll = QScrollArea()
        scroll.setWidget(result_frame)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background-color: transparent;")
        scroll.setMinimumHeight(200)

        # 3. Связи
        self.graph_manager.node_count_changed.connect(self.matrix_widget.update_size)

        # 4. Создание лейаутов
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Левая панель
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        
        # Матрица весов в GroupBox
        matrix_group = QGroupBox("📊 Матрица смежности")
        matrix_layout = QVBoxLayout(matrix_group)
        matrix_layout.addWidget(QLabel("Введите ненулевые значения для существующих связей:"))
        matrix_layout.addWidget(self.matrix_widget)
        left_layout.addWidget(matrix_group)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.clear_button)
        left_layout.addLayout(button_layout)
        
        # Кнопка решения
        left_layout.addWidget(self.solve_button)
        
        # Результаты
        left_layout.addWidget(scroll)
        
        # Правая панель
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(15)
        
        # Граф в GroupBox
        graph_group = QGroupBox("🎯 Граф")
        graph_layout = QVBoxLayout(graph_group)
        
        instructions = QLabel("""
            <b>Управление графом:</b><br>
            • <b>ЛКМ</b> по пустому месту — создать вершину<br>
            • <b>Shift + ЛКМ</b> по вершинам — создать ребро<br>
            • <b>ПКМ</b> по элементу — удалить<br>
            • <b>Перетаскивание</b> — перемещение вершин
        """)
        instructions.setStyleSheet("color: #7f8c8d; font-size: 13px; padding: 10px;")
        instructions.setWordWrap(True)
        graph_layout.addWidget(instructions)
        graph_layout.addWidget(self.view)
        
        right_layout.addWidget(graph_group)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

        self.setCentralWidget(central_widget)
        self.create_menu()

    def create_menu(self):
        menu = self.menuBar()
        menu.setStyleSheet("""
            QMenuBar {
                background-color: white;
                color: #2c3e50;
                border-bottom: 2px solid #e0e0e0;
                padding: 5px;
            }
            QMenuBar::item {
                padding: 5px 15px;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        file_menu = menu.addMenu("📁 Файл")
        file_menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            QMenu::item {
                padding: 8px 25px 8px 20px;
            }
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)

        save_action = QAction("💾 Сохранить упражнение...", self)
        save_action.triggered.connect(self.save_exercise)
        file_menu.addAction(save_action)

        load_action = QAction("📂 Загрузить упражнение...", self)
        load_action.triggered.connect(self.load_exercise)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        clear_action = QAction("🗑️ Очистить всё", self)
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)

    def solve_graph(self):
        # Анимация кнопки
        anim = QPropertyAnimation(self.solve_button, b"geometry")
        anim.setDuration(150)
        anim.setEasingCurve(QEasingCurve.Type.OutBack)
        anim.setStartValue(self.solve_button.geometry())
        anim.setEndValue(self.solve_button.geometry())
        anim.start()

        graph_struct = self.graph_manager.get_graph_structure() 
        matrix_struct = self.matrix_widget.get_structure()

        if not graph_struct:
            QMessageBox.warning(self, "Пустой граф", 
                              "❌ Граф пуст. Создайте вершины и рёбра.")
            self.result_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
            return
        
        solutions = GraphSolver.solve(graph_struct, matrix_struct)

        if not solutions:
            self.result_label.setText(
                "<span style='color: #e74c3c; font-weight: bold;'>❌ Решений не найдено.</span><br><br>"
                "<b>Возможные причины:</b><br>"
                "1. Структура графа не совпадает с отмеченными связями в таблице<br>"
                "2. Разное количество вершин в графе и матрице<br>"
                "3. Несовпадение степеней вершин"
            )
            self.result_label.setStyleSheet("color: #e74c3c; font-size: 14px;")
        else:
            text = f"<span style='color: #27ae60; font-weight: bold;'>✅ Найдено решений: {len(solutions)}</span><br>"
            text += "<hr style='border: 1px solid #e0e0e0;'>"
            
            for i, sol in enumerate(solutions):
                text += f"<b>Решение #{i+1}:</b><br>"
                sorted_items = sorted(sol.items(), key=lambda x: int(x[0]))
                row_str = []
                for num, letter in sorted_items:
                    row_str.append(f"<b>{num}</b> ➜ <span style='color: #3498db;'>{letter}</span>")
                text += "&nbsp;&nbsp;&nbsp;&nbsp;" + "&nbsp;&nbsp;&nbsp;&nbsp;".join(row_str) + "<br><br>"
            
            self.result_label.setText(text)
            self.result_label.setStyleSheet("color: #2c3e50; font-size: 14px;")

    def clear_all(self):
        self.graph_manager.reset()
        self.matrix_widget.update_size(0)
        self.result_label.setText("👈 Нарисуйте граф справа и заполните матрицу весов слева, затем нажмите 'Найти соответствие'")
        self.result_label.setStyleSheet("color: #2c3e50; font-size: 14px;")

    def save_exercise(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить упражнение", "", "JSON (*.json)")
        if not file_path: return

        nodes_data = []
        node_id_map = {}
        items = [i for i in self.scene.items() if isinstance(i, NodeItem)]
        items.sort(key=lambda x: x.name)
        
        for idx, node in enumerate(items):
            node_id_map[node] = idx
            nodes_data.append({
                "id": idx, "name": node.name,
                "x": node.pos().x(), "y": node.pos().y()
            })

        edges_data = []
        processed = set()
        for node in items:
            for edge in node.edges:
                if edge not in processed:
                    processed.add(edge)
                    u = node_id_map.get(edge.source)
                    v = node_id_map.get(edge.dest)
                    if u is not None and v is not None:
                        edges_data.append({"u": u, "v": v})

        data = {
            "graph": {"nodes": nodes_data, "edges": edges_data, "counter": self.graph_manager.node_counter},
            "matrix": self.matrix_widget.get_data()
        }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Успех", "✅ Упражнение успешно сохранено!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"❌ {str(e)}")

    def load_exercise(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить упражнение", "", "JSON (*.json)")
        if not file_path: return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.clear_all()
            
            g_data = data.get("graph", {})
            self.graph_manager.node_counter = g_data.get("counter", 0)
            
            id_map = {}
            for n in g_data.get("nodes", []):
                node = self.graph_manager.create_node(QPointF(n["x"], n["y"]), n["name"])
                id_map[n["id"]] = node
                
            for e in g_data.get("edges", []):
                u, v = id_map.get(e["u"]), id_map.get(e["v"])
                if u and v: self.graph_manager.create_edge(u, v)
            
            self.matrix_widget.set_data(data.get("matrix", []))
            
            QMessageBox.information(self, "Успех", "✅ Упражнение успешно загружено!")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"❌ {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Установка шрифта
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
