import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, 
                             QHeaderView, QFrame, QGroupBox, QSizePolicy)
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QLinearGradient
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve

class Interval:
    def __init__(self, name, start, end):
        self.name = name
        self.start = float(start)
        self.end = float(end)

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __repr__(self):
        return f"{self.name}: [{self.start}, {self.end}]"


class LogicSolver:
    def __init__(self, expression, intervals, search_range=(0, 100), step=0.5):
        self.expression = expression
        self.intervals = {i.name: i for i in intervals} 
        self.search_range = search_range
        self.step = step

    def check_expression(self, x, a_val_bool):
        context = {}
        for name, interval in self.intervals.items():
            context[name] = interval
        if a_val_bool:
            context['A'] = [x]
        else:
            context['A'] = []
        
        context['x'] = x

        try:
            return bool(eval(self.expression, {}, context))
        except Exception as e:
            raise ValueError(f"Ошибка в формуле: {e}")

    def solve(self, mode="min", target_value=True):
        points_in_a = []
        current = self.search_range[0]
        
        while current <= self.search_range[1]:
            res_without_a = self.check_expression(current, False)
            res_with_a = self.check_expression(current, True)
            
            if mode == "min":
                if res_without_a != target_value:
                    points_in_a.append(current)
            
            elif mode == "max":
                if res_with_a == target_value:
                    points_in_a.append(current)

            current += self.step
            current = round(current, 1)

        if not points_in_a:
            return None
        
        return Interval("A (Result)", min(points_in_a), max(points_in_a))

class IntervalChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(350)
        self.intervals = []
        self.result_interval = None
        self.bg_color = QColor(250, 250, 252)
        self.grid_color = QColor(220, 220, 230)
        self.accent_color = QColor(41, 128, 185)
        self.setStyleSheet("border-radius: 12px; background-color: #fafafc;")

    def update_data(self, intervals, result):
        self.intervals = intervals
        self.result_interval = result
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background with subtle gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(250, 250, 252))
        gradient.setColorAt(1, QColor(245, 247, 250))
        painter.fillRect(self.rect(), gradient)
        
        # Draw rounded border
        painter.setPen(QPen(QColor(220, 220, 230), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(1, 1, self.width()-2, self.height()-2, 12, 12)

        w = self.width()
        h = self.height()
        margin = 50
        axis_y = h - 70

        # Draw grid lines
        painter.setPen(QPen(self.grid_color, 1, Qt.PenStyle.DashLine))
        all_vals = [0, 50]
        for i in self.intervals:
            all_vals.extend([i.start, i.end])
        if self.result_interval:
            all_vals.extend([self.result_interval.start, self.result_interval.end])
        
        min_val = min(all_vals)
        max_val = max(all_vals)
        if max_val == min_val: max_val += 10
        scale_len = max_val - min_val
        if scale_len == 0: scale_len = 10
        
        px_per_unit = (w - 2 * margin) / scale_len

        def val_to_x(val):
            return margin + (val - min_val) * px_per_unit

        # Draw vertical grid lines
        step_grid = 10 if scale_len > 50 else 5
        if scale_len < 20: step_grid = 1
        
        current_grid = int(min_val)
        while current_grid <= int(max_val) + 1:
            x_pos = val_to_x(current_grid)
            if margin <= x_pos <= w - margin:
                painter.drawLine(int(x_pos), 30, int(x_pos), axis_y)
            current_grid += step_grid

        # Draw axis
        painter.setPen(QPen(QColor(70, 70, 80), 2))
        painter.drawLine(margin, axis_y, w - margin, axis_y)
        
        # Draw axis markers
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QPen(QColor(100, 100, 110)))
        current_grid = int(min_val)
        while current_grid <= int(max_val) + 1:
            x_pos = val_to_x(current_grid)
            if margin <= x_pos <= w - margin:
                painter.drawLine(int(x_pos), axis_y - 5, int(x_pos), axis_y + 5)
                painter.drawText(int(x_pos) - 10, axis_y + 25, str(current_grid))
            current_grid += step_grid

        # Draw axis label
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(margin - 40, axis_y - 10, "X")

        def draw_interval_bar(interval, y_pos, color, label, is_result=False):
            x1 = val_to_x(interval.start)
            x2 = val_to_x(interval.end)
            
            if x2 < margin or x1 > w - margin: 
                return
            
            x1 = max(x1, margin)
            x2 = min(x2, w - margin)
            
            width_bar = x2 - x1
            if width_bar < 3:
                width_bar = 3
                x1 -= 1.5
                
            height_bar = 28
            
            # Draw shadow for result
            if is_result:
                shadow_rect = QRectF(x1 + 3, y_pos + 3, width_bar, height_bar)
                painter.setBrush(QBrush(QColor(0, 0, 0, 30)))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(shadow_rect, 8, 8)
            
            # Draw main bar
            rect = QRectF(x1, y_pos, width_bar, height_bar)
            
            # Create gradient for bar
            bar_gradient = QLinearGradient(x1, y_pos, x1, y_pos + height_bar)
            if is_result:
                bar_gradient.setColorAt(0, QColor(231, 76, 60))
                bar_gradient.setColorAt(1, QColor(192, 57, 43))
            else:
                color_light = color.lighter(120)
                bar_gradient.setColorAt(0, color_light)
                bar_gradient.setColorAt(1, color)
            
            painter.setBrush(QBrush(bar_gradient))
            
            pen_width = 2 if is_result else 1
            pen_color = QColor(150, 40, 30) if is_result else color.darker(130)
            painter.setPen(QPen(pen_color, pen_width))
            
            painter.drawRoundedRect(rect, 8, 8)
            
            # Draw label
            painter.setPen(QPen(Qt.GlobalColor.white if is_result else Qt.GlobalColor.black, 1))
            font = QFont("Segoe UI", 10)
            if is_result:
                font.setBold(True)
            painter.setFont(font)
            
            label_text = f"{label} [{interval.start}, {interval.end}]"
            text_width = painter.fontMetrics().horizontalAdvance(label_text)
            if text_width < width_bar - 10:
                painter.drawText(int(x1 + 10), int(y_pos + height_bar/2 + 4), label_text)
            else:
                painter.drawText(int(x1 + 5), int(y_pos + height_bar/2 + 4), "...")

        # Draw intervals
        y_offset = axis_y - 45
        colors = [
            QColor(52, 152, 219),  # Blue
            QColor(46, 204, 113),  # Green
            QColor(155, 89, 182),  # Purple
            QColor(241, 196, 15),  # Yellow
            QColor(230, 126, 34),  # Orange
        ]
        
        for idx, interval in enumerate(self.intervals):
            color = colors[idx % len(colors)]
            draw_interval_bar(interval, y_offset, color, interval.name)
            y_offset -= 40

        # Draw result interval
        if self.result_interval:
            draw_interval_bar(self.result_interval, y_offset - 20, 
                            QColor(231, 76, 60), "Результат A", is_result=True)
        else:
            painter.setFont(QFont("Segoe UI", 12))
            painter.setPen(QPen(QColor(100, 100, 120)))
            painter.drawText(w//2 - 100, 50, "Результат: нет подходящих точек")

class MaterialButton(QPushButton):
    def __init__(self, text, color="#3498db"):
        super().__init__(text)
        self.color = QColor(color)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color.name()};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {self.color.darker(110).name()};
            }}
            QPushButton:pressed {{
                background-color: {self.color.darker(130).name()};
                padding: 11px 19px 9px 21px;
            }}
        """)

class MaterialLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)

class MaterialComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
        """)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Logic Interval Solver")
        self.resize(1100, 750)
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
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("🔍 Решатель логических интервалов")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px 0;
        """)
        main_layout.addWidget(header)

        # Formula section
        formula_group = QGroupBox("Логическое выражение")
        formula_layout = QVBoxLayout(formula_group)
        
        formula_hint = QLabel("Используйте: (x in P), and, or, not, <= (импликация), == (равенство)")
        formula_hint.setStyleSheet("color: #7f8c8d; font-size: 12px; padding-bottom: 5px;")
        formula_layout.addWidget(formula_hint)
        
        formula_input_layout = QHBoxLayout()
        formula_input_layout.addWidget(QLabel("Выражение:"))
        
        self.formula_input = MaterialLineEdit("(x in P) and (x in Q)")
        self.formula_input.setMinimumHeight(40)
        formula_input_layout.addWidget(self.formula_input)
        
        formula_layout.addLayout(formula_input_layout)
        main_layout.addWidget(formula_group)

        # Intervals table section
        table_group = QGroupBox("Интервалы")
        table_layout = QVBoxLayout(table_group)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя интервала", "Начало", "Конец"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setRowCount(2)
        
        # Set initial data
        for i, (name, start, end) in enumerate([("P", 0, 20), ("Q", 10, 30)]):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(str(start)))
            self.table.setItem(i, 2, QTableWidgetItem(str(end)))
        
        self.table.setStyleSheet("""
            QTableWidget {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #e0e0e0;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        table_layout.addWidget(self.table)
        
        # Table buttons
        table_buttons = QHBoxLayout()
        self.add_btn = MaterialButton("➕ Добавить интервал", "#2ecc71")
        self.add_btn.clicked.connect(lambda: self.add_interval_row("R", 15, 25))
        self.del_btn = MaterialButton("🗑️ Удалить", "#e74c3c")
        self.del_btn.clicked.connect(self.remove_row)
        
        table_buttons.addWidget(self.add_btn)
        table_buttons.addWidget(self.del_btn)
        table_buttons.addStretch()
        table_layout.addLayout(table_buttons)
        
        main_layout.addWidget(table_group)

        # Controls section
        controls_group = QGroupBox("Параметры решения")
        controls_layout = QHBoxLayout(controls_group)
        controls_layout.setSpacing(20)

        # Mode selection
        mode_widget = QWidget()
        mode_layout = QVBoxLayout(mode_widget)
        mode_layout.addWidget(QLabel("Режим поиска:"))
        self.mode_combo = MaterialComboBox()
        self.mode_combo.addItems(["Найти минимальный A", "Найти максимальный A"])
        mode_layout.addWidget(self.mode_combo)
        controls_layout.addWidget(mode_widget)

        # Target selection
        target_widget = QWidget()
        target_layout = QVBoxLayout(target_widget)
        target_layout.addWidget(QLabel("Требуемое значение:"))
        self.target_combo = MaterialComboBox()
        self.target_combo.addItems(["Тождественно истинно (1)", "Тождественно ложно (0)"])
        target_layout.addWidget(self.target_combo)
        controls_layout.addWidget(target_widget)

        # Calculate button
        self.calc_btn = MaterialButton("🚀 ВЫЧИСЛИТЬ", "#9b59b6")
        self.calc_btn.setMinimumHeight(50)
        self.calc_btn.clicked.connect(self.run_calculation)
        controls_layout.addWidget(self.calc_btn)
        
        main_layout.addWidget(controls_group)

        # Chart
        self.chart = IntervalChart()
        main_layout.addWidget(self.chart)

        # Result section
        result_frame = QFrame()
        result_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        result_layout = QHBoxLayout(result_frame)
        
        self.result_label = QLabel("⏳ Введите выражение и нажмите 'ВЫЧИСЛИТЬ'")
        self.result_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #2c3e50;
        """)
        result_layout.addWidget(self.result_label)
        
        main_layout.addWidget(result_frame)

    def add_interval_row(self, name, start, end):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(str(start)))
        self.table.setItem(row, 2, QTableWidgetItem(str(end)))

    def remove_row(self):
        row = self.table.currentRow()
        if row >= 0: 
            self.table.removeRow(row)

    def get_intervals_from_ui(self):
        intervals = []
        try:
            for row in range(self.table.rowCount()):
                name_item = self.table.item(row, 0)
                start_item = self.table.item(row, 1)
                end_item = self.table.item(row, 2)
                
                if not name_item or not start_item or not end_item:
                    continue
                    
                name = name_item.text().strip()
                start = float(start_item.text())
                end = float(end_item.text())
                
                if name:
                    intervals.append(Interval(name, start, end))
            return intervals
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "❌ Проверьте корректность чисел в таблице")
            return None
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"❌ Ошибка обработки данных: {str(e)}")
            return None

    def run_calculation(self):
        # Add button animation
        anim = QPropertyAnimation(self.calc_btn, b"geometry")
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.Type.OutBack)
        anim.setStartValue(self.calc_btn.geometry())
        anim.setEndValue(self.calc_btn.geometry())
        anim.start()

        intervals = self.get_intervals_from_ui()
        if intervals is None:
            return

        formula = self.formula_input.text().strip()
        if not formula:
            QMessageBox.warning(self, "Ошибка", "❌ Введите логическое выражение")
            return

        mode = "min" if self.mode_combo.currentIndex() == 0 else "max"
        target_is_true = (self.target_combo.currentIndex() == 0)

        try:
            # Calculate max search range
            all_coords = [i.end for i in intervals]
            max_search = max(all_coords) * 1.5 if all_coords else 100
            
            solver = LogicSolver(formula, intervals, search_range=(0, max_search))
            result_a = solver.solve(mode=mode, target_value=target_is_true)
            
            # Update chart
            self.chart.update_data(intervals, result_a)
            
            # Update result label
            target_text = "истинно (1)" if target_is_true else "ложно (0)"
            mode_text = "минимальный" if mode == "min" else "максимальный"
            
            if result_a:
                self.result_label.setText(
                    f"✅ Чтобы выражение было {target_text}, {mode_text} отрезок A: "
                    f"[{result_a.start:.2f}, {result_a.end:.2f}]"
                )
                self.result_label.setStyleSheet("color: #27ae60; font-size: 15px; font-weight: bold;")
            else:
                self.result_label.setText(
                    f"⚠️ Для выражения = {target_text} решение не найдено (пустое множество)"
                )
                self.result_label.setStyleSheet("color: #f39c12; font-size: 15px; font-weight: bold;")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка вычисления", f"❌ {str(e)}")
            self.result_label.setText("❌ Ошибка вычисления")
            self.result_label.setStyleSheet("color: #c0392b; font-size: 15px; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())