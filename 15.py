import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QHeaderView)
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PySide6.QtCore import Qt, QRectF


class Interval:
    def __init__(self, name, start, end):
        self.name = name
        self.start = float(start)
        self.end = float(end)

    def __contains__(self, item):
        return self.start <= item <= self.end

    def __repr__(self):
        return f"{self.name}: [{self.start:.2f}, {self.end:.2f}]"


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
        current = self.search_range[0]
        segments = []
        current_segment_start = None
        
        while current <= self.search_range[1]:
            res_without_a = self.check_expression(current, False)
            res_with_a = self.check_expression(current, True)
            
            condition_met = False
            if mode == "min":
                condition_met = (res_without_a != target_value)
            elif mode == "max":
                condition_met = (res_with_a == target_value)
            
            if condition_met:
                if current_segment_start is None:
                    current_segment_start = current
            else:
                if current_segment_start is not None:
                    segments.append((current_segment_start, current - self.step))
                    current_segment_start = None
            
            current += self.step
            current = round(current, 2)
        
        if current_segment_start is not None:
            segments.append((current_segment_start, min(current - self.step, self.search_range[1])))
        
        if not segments:
            return None
        
        if mode == "min":
            return Interval("A (Result)", segments[0][0], segments[0][1])
        elif mode == "max":
            return Interval("A (Result)", segments[-1][0], segments[-1][1])


class IntervalChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(350)
        self.intervals = []
        self.result_interval = None

    def update_data(self, intervals, result):
        self.intervals = intervals
        self.result_interval = result
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        w = self.width()
        h = self.height()
        margin = 40
        axis_y = h - 80

        all_vals = [0, 50]
        for i in self.intervals:
            all_vals.extend([i.start, i.end])
        if self.result_interval:
            all_vals.extend([self.result_interval.start, self.result_interval.end])
        
        min_val = min(all_vals)
        max_val = max(all_vals)
        if max_val == min_val: 
            max_val += 10
        
        scale_len = max_val - min_val
        if scale_len == 0: 
            scale_len = 10
        
        px_per_unit = (w - 2 * margin) / scale_len

        def val_to_x(val):
            return margin + (val - min_val) * px_per_unit

        # Ось
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawLine(margin, axis_y, w - margin, axis_y)
        
        # Деления
        painter.setFont(QFont("Arial", 8))
        step_grid = 10
        current_grid = int(min_val)
        while current_grid <= int(max_val) + 1:
            x_pos = val_to_x(current_grid)
            if margin <= x_pos <= w - margin:
                painter.drawLine(int(x_pos), axis_y - 5, int(x_pos), axis_y + 5)
                painter.drawText(int(x_pos) - 10, axis_y + 20, str(current_grid))
            current_grid += step_grid

        def draw_interval_bar(interval, y_pos, color, label, is_result=False):
            x1 = val_to_x(interval.start)
            x2 = val_to_x(interval.end)
            
            x1_clipped = max(x1, margin)
            x2_clipped = min(x2, w - margin)
            
            width_bar = x2_clipped - x1_clipped
            height_bar = 25
            
            rect = QRectF(x1_clipped, y_pos, width_bar, height_bar)
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawRect(rect)
            
            # Текст
            if is_result:
                coord_text = f"[{interval.start:.1f}, {interval.end:.1f}]"
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
                text_width = painter.fontMetrics().horizontalAdvance(coord_text)
                
                if width_bar > text_width + 10:
                    painter.drawText(int(x1_clipped + (width_bar - text_width) / 2), 
                                   int(y_pos + height_bar/2 + 4), coord_text)
                
                # Длина
                length = interval.end - interval.start
                length_text = f"Длина: {length:.1f}"
                painter.drawText(int(x1_clipped + (width_bar - painter.fontMetrics().horizontalAdvance(length_text)) / 2),
                               int(y_pos + height_bar + 15), length_text)
            else:
                label_text = f"{label}"
                painter.setPen(QPen(Qt.GlobalColor.black, 1))
                painter.setFont(QFont("Arial", 9))
                text_width = painter.fontMetrics().horizontalAdvance(label_text)
                
                if text_width < width_bar - 10:
                    painter.drawText(int(x1_clipped + 5), int(y_pos + height_bar/2 + 4), label_text)

        # Интервалы
        y_offset = axis_y - 40
        colors = [
            QColor(200, 230, 255),  # Светло-голубой
            QColor(200, 255, 200),  # Светло-зеленый
            QColor(255, 230, 200),  # Светло-оранжевый
            QColor(255, 200, 255),  # Светло-фиолетовый
        ]
        
        for idx, interval in enumerate(self.intervals):
            color = colors[idx % len(colors)]
            draw_interval_bar(interval, y_offset, color, interval.name)
            y_offset -= 35

        # Результат
        if self.result_interval:
            result_y = axis_y - 120
            
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            painter.setPen(QPen(QColor(0, 0, 200)))
            painter.drawText(margin, result_y - 20, "РЕЗУЛЬТАТ:")
            
            draw_interval_bar(self.result_interval, result_y, 
                            QColor(180, 220, 255), "A", is_result=True)
        else:
            painter.setFont(QFont("Arial", 11))
            painter.setPen(QPen(QColor(100, 100, 100)))
            painter.drawText(w//2 - 80, 50, "Результат не найден")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logic Solver")
        self.resize(900, 700)
        
        # Простые цвета
        self.setStyleSheet("""
            QMainWindow {
                background-color: #E0E0E0;
            }
            QLabel {
                font-size: 12px;
                font-family: Arial;
                color: black;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(8)

        # Заголовок
        header = QLabel("Решатель логических интервалов")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        main_layout.addWidget(header)

        # Формула
        formula_widget = QWidget()
        formula_layout = QVBoxLayout(formula_widget)

        # Заголовок без рамки
        formula_title = QLabel("Формула")
        formula_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px; color: black;")
        formula_layout.addWidget(formula_title)

        formula_layout.addWidget(QLabel("Логическое выражение:"))

        self.formula_input = QLineEdit()
        self.formula_input.setPlaceholderText("(x in P) and (x in Q)")
        self.formula_input.setStyleSheet("padding: 5px; border: 1px solid gray;")
        formula_layout.addWidget(self.formula_input)

        formula_layout.addWidget(QLabel("(x in P), and, or, not, <=, =="))

        main_layout.addWidget(formula_widget)

        # Таблица интервалов
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)

        # Заголовок таблицы
        table_title = QLabel("Интервалы")
        table_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px; color: black;")
        table_layout.addWidget(table_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя", "Начало", "Конец"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(2)
        self.table.setStyleSheet("border: 1px solid gray; background-color: white;")
        
        # Начальные данные
        for i, (name, start, end) in enumerate([("P", 0, 20), ("Q", 10, 30)]):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(str(start)))
            self.table.setItem(i, 2, QTableWidgetItem(str(end)))
        
        table_layout.addWidget(self.table)
        
        # Кнопки таблицы
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(lambda: self.add_interval_row("R", 15, 25))
        self.add_btn.setStyleSheet("padding: 5px 10px; background-color: green; border: 1px solid gray; color: black;")
        
        self.del_btn = QPushButton("Удалить")
        self.del_btn.clicked.connect(self.remove_row)
        self.del_btn.setStyleSheet("padding: 5px 10px; background-color: red; border: 1px solid gray; color: black;")
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.del_btn)
        buttons_layout.addStretch()
        
        table_layout.addLayout(buttons_layout)
        main_layout.addWidget(table_widget)

        # Настройки
        settings_widget = QWidget()
        settings_layout = QHBoxLayout(settings_widget)

        # Заголовок настроек
        settings_title = QLabel("Настройки")
        settings_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px; color: black;")
        main_layout.addWidget(settings_title)
        
        # Режим
        mode_widget = QWidget()
        mode_layout = QVBoxLayout(mode_widget)
        mode_layout.addWidget(QLabel("Режим:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Минимальный A", "Максимальный A"])
        self.mode_combo.setStyleSheet("padding: 3px; border: 1px solid gray; background-color: white;")
        mode_layout.addWidget(self.mode_combo)
        settings_layout.addWidget(mode_widget)

        # Целевое значение
        target_widget = QWidget()
        target_layout = QVBoxLayout(target_widget)
        target_layout.addWidget(QLabel("Значение:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(["Истина (1)", "Ложь (0)"])
        self.target_combo.setStyleSheet("padding: 3px; border: 1px solid gray; background-color: white;")
        target_layout.addWidget(self.target_combo)
        settings_layout.addWidget(target_widget)

        # Кнопка вычисления
        self.calc_btn = QPushButton("ВЫЧИСЛИТЬ")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self.run_calculation)
        self.calc_btn.setStyleSheet("""
            padding: 8px 20px; 
            background-color: blue; 
            border: 2px solid gray;
            font-weight: bold;
            color: white;
        """)
        settings_layout.addWidget(self.calc_btn)
        
        main_layout.addWidget(settings_widget)

        # График
        chart_widget = QWidget()
        chart_layout = QVBoxLayout(chart_widget)

        # Заголовок графика
        chart_title = QLabel("График")
        chart_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 5px; color: black;")
        chart_layout.addWidget(chart_title)
        
        self.chart = IntervalChart()
        chart_layout.addWidget(self.chart)
        
        main_layout.addWidget(chart_widget)

        # Результат
        result_widget = QWidget()
        result_layout = QHBoxLayout(result_widget)
        result_widget.setStyleSheet("background-color: white; padding: 8px;")
        
        self.result_label = QLabel("Введите данные и нажмите ВЫЧИСЛИТЬ")
        self.result_label.setStyleSheet("font-weight: bold; color: black;")
        result_layout.addWidget(self.result_label)
        
        main_layout.addWidget(result_widget)

    # МЕТОДЫ КЛАССА
    
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
        except:
            QMessageBox.warning(self, "Ошибка", "Неправильные числа в таблице")
            return None

    def run_calculation(self):
        intervals = self.get_intervals_from_ui()
        if intervals is None:
            return

        formula = self.formula_input.text().strip()
        if not formula:
            QMessageBox.warning(self, "Ошибка", "Введите формулу")
            return

        mode = "min" if self.mode_combo.currentIndex() == 0 else "max"
        target_is_true = (self.target_combo.currentIndex() == 0)

        try:
            all_coords = [i.end for i in intervals]
            max_search = max(all_coords) * 1.5 if all_coords else 100
            
            solver = LogicSolver(formula, intervals, search_range=(0, max_search))
            result_a = solver.solve(mode=mode, target_value=target_is_true)
            
            self.chart.update_data(intervals, result_a)
            
            target_text = "истинно" if target_is_true else "ложно"
            mode_text = "минимальный" if mode == "min" else "максимальный"
            
            if result_a:
                length = result_a.end - result_a.start
                self.result_label.setText(
                    f"Отрезок A: [{result_a.start:.2f}, {result_a.end:.2f}] "
                    f"(длина: {length:.2f})"
                )
                self.result_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.result_label.setText("Решение не найдено")
                self.result_label.setStyleSheet("color: orange; font-weight: bold;")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.result_label.setText("Ошибка вычисления")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
