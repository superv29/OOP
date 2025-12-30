import tkinter as tk
from tkinter import messagebox
from itertools import permutations


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Point:
    #Класс вершины графа
    def __init__(self, x, y, letter_id):
        self.x = x
        self.y = y
        self.letter_id = letter_id
        self.connections = []
        self.canvas_oval_id = None
        self.canvas_text_id = None


class Edge:
    #Класс ребра графа
    def __init__(self, point1_id, point2_id):
        self.points = [point1_id, point2_id]
        self.canvas_line_id = None


class GraphCanvas(tk.Canvas):
    #Канвас для рисования графа
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.points = {}
        self.edges = []
        self.next_letter_idx = 0
        self.point_radius = 20
        self.edge_click_tolerance = 8
        
        # Для рисования рёбер
        self.edge_start_point = None
        self.temp_line = None
        
        # Для перетаскивания вершин
        self.drag_point = None
        
        # Привязка событий мыши
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        self.bind('<Button-3>', self.on_right_click)
    
    def get_point_at(self, x, y):
        #Находит вершину по координатам
        for letter_id, point in self.points.items():
            dist = ((point.x - x) ** 2 + (point.y - y) ** 2) ** 0.5
            if dist <= self.point_radius:
                return point
        return None
    
    def get_edge_at(self, x, y):
        #Находит ребро по координатам
        for edge in self.edges:
            p1 = self.points[edge.points[0]]
            p2 = self.points[edge.points[1]]
            dist = self.point_to_segment_distance(x, y, p1.x, p1.y, p2.x, p2.y)
            if dist <= self.edge_click_tolerance:
                return edge
        return None
    
    def point_to_segment_distance(self, px, py, x1, y1, x2, y2):
        #Вычисляет расстояние от точки до отрезка
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        
        return ((px - proj_x) ** 2 + (py - proj_y) ** 2) ** 0.5
    
    def on_click(self, event):
        #Обработка клика ЛКМ
        point = self.get_point_at(event.x, event.y)
        
        if point:
            # Проверяем, зажат ли Shift
            if event.state & 0x1:  # Shift зажат
                # Начинаем перетаскивание вершины
                self.drag_point = point
            else:
                # Начинаем рисование ребра
                self.edge_start_point = point
        else:
            # Добавляем новую вершину
            self.add_point(event.x, event.y)
    
    def on_drag(self, event):
        #Обработка перетаскивания
        if self.drag_point:
            # Режим перетаскивания вершины
            self.move_point_to(self.drag_point, event.x, event.y)
        
        elif self.edge_start_point:
            # Режим рисования ребра — показываем пунктирную линию
            if self.temp_line:
                self.delete(self.temp_line)
            self.temp_line = self.create_line(
                self.edge_start_point.x, self.edge_start_point.y,
                event.x, event.y,
                fill='gray', dash=(4, 4), width=2
            )
    
    def on_release(self, event):
        #Обработка отпускания кнопки мыши
        # Удаляем временную линию
        if self.temp_line:
            self.delete(self.temp_line)
            self.temp_line = None
        
        # Если рисовали ребро
        if self.edge_start_point:
            end_point = self.get_point_at(event.x, event.y)
            if end_point and end_point != self.edge_start_point:
                self.add_edge(self.edge_start_point, end_point)
            self.edge_start_point = None
        
        # Если перетаскивали вершину
        if self.drag_point:
            self.drag_point = None
    
    def move_point_to(self, point, x, y):
        #Перемещает вершину в указанные координаты
        point.x = x
        point.y = y
        
        # Перемещаем овал
        self.coords(
            point.canvas_oval_id,
            point.x - self.point_radius, point.y - self.point_radius,
            point.x + self.point_radius, point.y + self.point_radius
        )
        
        # Перемещаем текст
        self.coords(point.canvas_text_id, point.x, point.y)
        
        # Перерисовываем все связанные рёбра
        for edge in self.edges:
            if point.letter_id in edge.points:
                p1 = self.points[edge.points[0]]
                p2 = self.points[edge.points[1]]
                self.coords(edge.canvas_line_id, p1.x, p1.y, p2.x, p2.y)
    
    def on_right_click(self, event):
        #ПКМ - удаление вершины или ребра
        point = self.get_point_at(event.x, event.y)
        if point:
            self.delete_point(point)
            return
        
        edge = self.get_edge_at(event.x, event.y)
        if edge:
            self.delete_edge(edge)
    
    def add_point(self, x, y):
        #Добавление новой вершины
        if self.next_letter_idx >= len(LETTERS):
            messagebox.showwarning("Предупреждение", "Достигнуто максимальное количество вершин")
            return
        
        letter = LETTERS[self.next_letter_idx]
        self.next_letter_idx += 1
        
        point = Point(x, y, letter)
        point.canvas_oval_id = self.create_oval(
            x - self.point_radius, y - self.point_radius,
            x + self.point_radius, y + self.point_radius,
            fill='lightblue', outline='darkblue', width=2
        )
        point.canvas_text_id = self.create_text(
            x, y, text=letter, font=('Arial', 14, 'bold')
        )
        
        self.points[letter] = point
    
    def delete_point(self, point):
        #Удаление вершины и всех связанных рёбер
        edges_to_remove = [e for e in self.edges if point.letter_id in e.points]
        for edge in edges_to_remove:
            self.delete(edge.canvas_line_id)
            self.edges.remove(edge)
            other_id = edge.points[0] if edge.points[1] == point.letter_id else edge.points[1]
            if other_id in self.points:
                if point.letter_id in self.points[other_id].connections:
                    self.points[other_id].connections.remove(point.letter_id)
        
        self.delete(point.canvas_oval_id)
        self.delete(point.canvas_text_id)
        del self.points[point.letter_id]
    
    def delete_edge(self, edge):
        #Удаление ребра
        point1_id, point2_id = edge.points
        
        self.delete(edge.canvas_line_id)
        self.edges.remove(edge)
        
        if point1_id in self.points and point2_id in self.points[point1_id].connections:
            self.points[point1_id].connections.remove(point2_id)
        if point2_id in self.points and point1_id in self.points[point2_id].connections:
            self.points[point2_id].connections.remove(point1_id)
    
    def add_edge(self, point1, point2):
        #Добавление ребра между вершинами
        for edge in self.edges:
            if set(edge.points) == {point1.letter_id, point2.letter_id}:
                return
        
        edge = Edge(point1.letter_id, point2.letter_id)
        edge.canvas_line_id = self.create_line(
            point1.x, point1.y, point2.x, point2.y,
            fill='black', width=3
        )
        for p in [point1, point2]:
            self.tag_raise(p.canvas_oval_id)
            self.tag_raise(p.canvas_text_id)
        
        self.edges.append(edge)
        point1.connections.append(point2.letter_id)
        point2.connections.append(point1.letter_id)
    
    def get_adjacency_matrix(self):
        #Возвращает матрицу смежности и список вершин
        vertices = sorted(self.points.keys())
        n = len(vertices)
        matrix = [[0] * n for _ in range(n)]
        
        for i, v1 in enumerate(vertices):
            for j, v2 in enumerate(vertices):
                if v2 in self.points[v1].connections:
                    matrix[i][j] = 1
        
        return matrix, vertices
    
    def clear_all(self):
        #Очистка канваса
        self.delete("all")
        self.points = {}
        self.edges = []
        self.next_letter_idx = 0


class AdjacencyMatrixTable(tk.Frame):
    #Таблица для ввода матрицы смежности
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.matrix = []
        self.buttons = []
        self.n = 0
        self.build_table()
    
    def build_table(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.buttons = []
        
        tk.Label(self, text="", width=4, height=2).grid(row=0, column=0)
        
        for j in range(self.n):
            btn = tk.Button(
                self, text=str(j + 1), width=4, height=1,
                command=lambda c=j: self.delete_vertex(c),
                bg='#FFE4B5', font=('Arial', 10, 'bold'),
                cursor='hand2'
            )
            btn.grid(row=0, column=j + 1, padx=1, pady=1)
        
        tk.Button(
            self, text="+", width=4, height=1,
            command=self.add_vertex, bg='#90EE90',
            font=('Arial', 10, 'bold'), cursor='hand2'
        ).grid(row=0, column=self.n + 1, padx=1, pady=1)
        
        for i in range(self.n):
            btn = tk.Button(
                self, text=str(i + 1), width=4, height=1,
                command=lambda r=i: self.delete_vertex(r),
                bg='#FFE4B5', font=('Arial', 10, 'bold'),
                cursor='hand2'
            )
            btn.grid(row=i + 1, column=0, padx=1, pady=1)
            
            row_buttons = []
            for j in range(self.n):
                if i == j:
                    btn = tk.Button(
                        self, text="—", width=4, height=1,
                        state='disabled', bg='#D3D3D3',
                        disabledforeground='#808080'
                    )
                else:
                    val = self.matrix[i][j] if i < len(self.matrix) and j < len(self.matrix[i]) else 0
                    bg = '#90EE90' if val == 1 else 'white'
                    btn = tk.Button(
                        self, text=str(val), width=4, height=1,
                        command=lambda r=i, c=j: self.toggle_cell(r, c),
                        bg=bg, font=('Arial', 10), cursor='hand2'
                    )
                btn.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        tk.Button(
            self, text="+", width=4, height=1,
            command=self.add_vertex, bg='#90EE90',
            font=('Arial', 10, 'bold'), cursor='hand2'
        ).grid(row=self.n + 1, column=0, padx=1, pady=1)
    
    def add_vertex(self):
        self.n += 1
        for row in self.matrix:
            row.append(0)
        self.matrix.append([0] * self.n)
        self.build_table()
    
    def delete_vertex(self, idx):
        if self.n <= 0:
            return
        del self.matrix[idx]
        for row in self.matrix:
            del row[idx]
        self.n -= 1
        self.build_table()
    
    def toggle_cell(self, i, j):
        if i == j:
            return
        new_val = 1 - self.matrix[i][j]
        self.matrix[i][j] = new_val
        self.matrix[j][i] = new_val
        bg = '#90EE90' if new_val == 1 else 'white'
        self.buttons[i][j].config(text=str(new_val), bg=bg)
        self.buttons[j][i].config(text=str(new_val), bg=bg)
    
    def get_matrix(self):
        return [row[:] for row in self.matrix]
    
    def clear_all(self):
        self.matrix = []
        self.n = 0
        self.build_table()


def solve(graph_matrix, graph_vertices, user_matrix):
    n = len(user_matrix)
    if len(graph_vertices) != n:
        return None, None
    if n == 0:
        return [], []
    
    for perm in permutations(range(n)):
        permuted_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                permuted_matrix[i][j] = graph_matrix[perm[i]][perm[j]]
        
        if permuted_matrix == user_matrix:
            numbers = list(range(1, n + 1))
            letters = [graph_vertices[perm[i]] for i in range(n)]
            return numbers, letters
    
    return None, None


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор графов — Изоморфизм")
        self.geometry("1100x750")
        self.configure(bg='#F0F0F0')
        self.create_widgets()
    
    def create_widgets(self):
        top_frame = tk.Frame(self, bg='#F0F0F0')
        top_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas_frame = tk.LabelFrame(
            top_frame, 
            text="Граф: ЛКМ — точка/ребро | Shift+ЛКМ — перемещение | ПКМ — удалить",
            font=('Arial', 10, 'bold'), bg='#F0F0F0'
        )
        canvas_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        self.canvas = GraphCanvas(canvas_frame, bg='white', width=500, height=450)
        self.canvas.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Button(
            canvas_frame, text="Очистить граф", command=self.canvas.clear_all,
            bg='#FFB6C1', font=('Arial', 9)
        ).pack(pady=5)
        
        table_frame = tk.LabelFrame(
            top_frame,
            text="Матрица смежности (клик на номер — удалить)",
            font=('Arial', 10, 'bold'), bg='#F0F0F0'
        )
        table_frame.pack(side='right', fill='both', padx=5)
        
        table_container = tk.Frame(table_frame, bg='#F0F0F0')
        table_container.pack(padx=10, pady=10)
        
        self.adj_table = AdjacencyMatrixTable(table_container)
        self.adj_table.pack()
        
        tk.Button(
            table_frame, text="Очистить матрицу", command=self.adj_table.clear_all,
            bg='#FFB6C1', font=('Arial', 9)
        ).pack(pady=5)
        
        tk.Button(
            self, text="РЕШИТЬ", command=self.solve,
            font=('Arial', 14, 'bold'), bg='#87CEEB',
            width=20, height=2, cursor='hand2'
        ).pack(pady=10)
        
        self.result_frame = tk.LabelFrame(
            self, text="Результат", 
            font=('Arial', 10, 'bold'), bg='#F0F0F0'
        )
        self.result_frame.pack(fill='x', padx=10, pady=10)
    
    def solve(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        graph_matrix, graph_vertices = self.canvas.get_adjacency_matrix()
        user_matrix = self.adj_table.get_matrix()
        
        if len(graph_vertices) == 0:
            messagebox.showwarning("Предупреждение", "Граф пуст!")
            return
        
        if len(user_matrix) == 0:
            messagebox.showwarning("Предупреждение", "Матрица смежности пуста!")
            return
        
        if len(graph_vertices) != len(user_matrix):
            messagebox.showerror(
                "Ошибка",
                f"Вершин в графе: {len(graph_vertices)}, размер матрицы: {len(user_matrix)}"
            )
            return
        
        numbers, letters = solve(graph_matrix, graph_vertices, user_matrix)
        
        if numbers is None:
            tk.Label(
                self.result_frame,
                text="❌ Соответствие не найдено. Графы не изоморфны.",
                font=('Arial', 12, 'bold'), fg='red', bg='#F0F0F0'
            ).pack(pady=10)
            return
        
        tk.Label(
            self.result_frame,
            text="✓ Найдено соответствие:",
            font=('Arial', 12, 'bold'), fg='green', bg='#F0F0F0'
        ).pack(pady=5)
        
        result_table = tk.Frame(self.result_frame, bg='#F0F0F0')
        result_table.pack(pady=10)
        
        tk.Label(
            result_table, text="Номер:", 
            font=('Arial', 11, 'bold'), bg='#F0F0F0', width=8
        ).grid(row=0, column=0, padx=2)
        
        for i, num in enumerate(numbers):
            tk.Label(
                result_table, text=str(num), width=4, height=2,
                relief='ridge', font=('Arial', 12, 'bold'), bg='#FFE4B5'
            ).grid(row=0, column=i + 1, padx=2, pady=2)
        
        tk.Label(
            result_table, text="Вершина:",
            font=('Arial', 11, 'bold'), bg='#F0F0F0', width=8
        ).grid(row=1, column=0, padx=2)
        
        for i, letter in enumerate(letters):
            tk.Label(
                result_table, text=letter, width=4, height=2,
                relief='ridge', font=('Arial', 12, 'bold'), bg='#ADD8E6'
            ).grid(row=1, column=i + 1, padx=2, pady=2)


if __name__ == '__main__':
    app = GraphApp()
    app.mainloop()
