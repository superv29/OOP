import tkinter as tk
from tkinter import ttk
from abc import *

class Solver(ABC):
    def __init__(self):
        self._win_rocks = None
        self._operations = None
        self._type = None
        self._conditions = None
        self._bad_move = None

    def __set_win_rocks(self, count): self._win_rocks = count
    def __set_operations(self, operations): self._operations = operations
    def __set_type(self, type): self._type = type
    def __set_conditions(self, cond): self._conditions = cond
    def __set_bad_move(self, flag): self._bad_move = flag

    WinRocks = property(lambda x: x._win_rocks, __set_win_rocks)
    Operations = property(lambda x: x._operations, __set_operations)
    Type = property(lambda x: x._type, __set_type)
    Conditions = property(lambda x: x._conditions, __set_conditions)
    BadMove = property(lambda x: x._bad_move, __set_bad_move)

    @abstractmethod
    def solve_task_19(self): pass
    @abstractmethod
    def solve_task_20(self): pass
    @abstractmethod
    def solve_task_21(self): pass

class Solver_1_Heap(Solver):
    def __init__(self):
        super().__init__()
        self._type = "1"

    def solve_task_19(self):
        if self.Operations[0][0] in ("*", "+"):
            for s in range(1, self.Conditions):
                if self.__func_19(s, 1): return s
        else:
            for s in range(self.Conditions, self.Conditions*100):
                if self.__func_19(s, 1): return s
        return "N/A"
                
    def solve_task_20(self):
        answers = []
        rng = range(1, self.Conditions) if self.Operations[0][0] in ("*", "+") else range(self.Conditions, self.Conditions*100)
        for s in rng:
            if self.__func_20(s, 1): answers.append(s)
        return ", ".join(map(str, answers)) if answers else "N/A"
    
    def solve_task_21(self):
        temps = []
        rng = range(1, self.Conditions) if self.Operations[0][0] in ("*", "+") else range(self.Conditions, self.Conditions*100)
        for s in rng:
            if self.__func_21(s, 1): temps.append(s)
        
        results = []
        for s in temps:
            if not self.__func_21_correct(s, 1):
                results.append(s)
        return results[0] if results else "N/A"

    def __func_19(self, x, h):
        if self.Operations[0][0] in ("*", "+"):
            if x >= self.WinRocks and h == 3: return True
            if x < self.WinRocks and h == 3: return False
            if x >= self.WinRocks: return False
        else:
            if x <= self.WinRocks and h == 3: return True
            if x > self.WinRocks and h == 3: return False
            if x <= self.WinRocks: return False 

        moves = [eval(f"{x}{op}") for op in self.Operations]
        if self.BadMove and h == 1:
            return any(self.__func_19(m, h+1) for m in moves)
        
        if h % 2 == 1:
            return all(self.__func_19(m, h+1) for m in moves)
        else:
            return any(self.__func_19(m, h+1) for m in moves)
    
    def __func_20(self, x, h):
        if self.Operations[0][0] in ("*", "+"):
            if x >= self.WinRocks and h == 4: return True
            if x < self.WinRocks and h == 4: return False
            if x >= self.WinRocks: return False
        else:
            if x <= self.WinRocks and h == 4: return True
            if x > self.WinRocks and h == 4: return False
            if x <= self.WinRocks: return False 

        moves = [eval(f"{x}{op}") for op in self.Operations]
        if h % 2 == 0:
            return all(self.__func_20(m, h+1) for m in moves)
        else:
            return any(self.__func_20(m, h+1) for m in moves)

    def __func_21(self, x, h):
        if self.Operations[0][0] in ("*", "+"):
            if x >= self.WinRocks and (h == 3 or h == 5): return True
            if x < self.WinRocks and h == 5: return False
            if x >= self.WinRocks and h < 5: return False
        else:
            if x <= self.WinRocks and (h == 3 or h == 5): return True
            if x > self.WinRocks and h == 5: return False
            if x <= self.WinRocks and h < 5: return False 

        moves = [eval(f"{x}{op}") for op in self.Operations]
        if h % 2 == 1:
            return all(self.__func_21(m, h+1) for m in moves)
        else:
            return any(self.__func_21(m, h+1) for m in moves)

    def __func_21_correct(self, x, h):
        if self.Operations[0][0] in ("*", "+"):
            if x >= self.WinRocks and h == 3: return True
            if x < self.WinRocks and h == 3: return False
            if x >= self.WinRocks and h < 3: return False
        else:
            if x <= self.WinRocks and h == 3: return True
            if x > self.WinRocks and h == 3: return False
            if x <= self.WinRocks and h < 3: return False 
        
        moves = [eval(f"{x}{op}") for op in self.Operations]
        if h % 2 == 1:
            return all(self.__func_21_correct(m, h+1) for m in moves)
        else:
            return any(self.__func_21_correct(m, h+1) for m in moves)

class Solver_2_Heap(Solver):
    def __init__(self):
        super().__init__()
        self._type = "2"
        self._start_rocks = None
    
    def __set_start_rocks(self, start): self._start_rocks = start
    StartRocks = property(lambda x: x._start_rocks, __set_start_rocks)

    def solve_task_19(self):
        rng = range(1, self.Conditions) if self.Operations[0][0] in ("*", "+") else range(self.Conditions, self.Conditions*100)
        for s in rng:
            if self.__func_19(s, self.StartRocks, 1): return s
        return "N/A"

    def solve_task_20(self):
        answers = []
        rng = range(1, self.Conditions) if self.Operations[0][0] in ("*", "+") else range(self.Conditions, self.Conditions*100)
        for s in rng:
            if self.__func_20(s, self.StartRocks, 1): answers.append(s)
        return ", ".join(map(str, answers)) if answers else "N/A"

    def solve_task_21(self):
        temps = []
        rng = range(1, self.Conditions) if self.Operations[0][0] in ("*", "+") else range(self.Conditions, self.Conditions*100)
        for s in rng:
            if self.__func_21(s, self.StartRocks, 1): temps.append(s)
        
        results = []
        for s in temps:
            if not self.__func_21_correct(s, self.StartRocks, 1):
                results.append(s)
        return results[0] if results else "N/A"

    def __func_19(self, x, y, h):
        win = (x + y >= self.WinRocks) if self.Operations[0][0] in ("*", "+") else (x + y <= self.WinRocks)
        if win and h == 3: return True
        if not win and h == 3: return False
        if win: return False

        moves = []
        for op in self.Operations:
            moves.append((eval(f"{x}{op}"), y))
            moves.append((x, eval(f"{y}{op}")))
        
        if self.BadMove and h == 1:
            return any(self.__func_19(m[0], m[1], h+1) for m in moves)

        if h % 2 == 1:
            return all(self.__func_19(m[0], m[1], h+1) for m in moves)
        else:
            return any(self.__func_19(m[0], m[1], h+1) for m in moves)

    def __func_20(self, x, y, h):
        win = (x + y >= self.WinRocks) if self.Operations[0][0] in ("*", "+") else (x + y <= self.WinRocks)
        if win and h == 4: return True
        if not win and h == 4: return False
        if win: return False

        moves = []
        for op in self.Operations:
            moves.append((eval(f"{x}{op}"), y))
            moves.append((x, eval(f"{y}{op}")))

        if h % 2 == 0:
            return all(self.__func_20(m[0], m[1], h+1) for m in moves)
        else:
            return any(self.__func_20(m[0], m[1], h+1) for m in moves)

    def __func_21(self, x, y, h):
        win = (x + y >= self.WinRocks) if self.Operations[0][0] in ("*", "+") else (x + y <= self.WinRocks)
        if win and (h == 3 or h == 5): return True
        if not win and h == 5: return False
        if win and h < 5: return False

        moves = []
        for op in self.Operations:
            moves.append((eval(f"{x}{op}"), y))
            moves.append((x, eval(f"{y}{op}")))

        if h % 2 == 1:
            return all(self.__func_21(m[0], m[1], h+1) for m in moves)
        else:
            return any(self.__func_21(m[0], m[1], h+1) for m in moves)

    def __func_21_correct(self, x, y, h):
        win = (x + y >= self.WinRocks) if self.Operations[0][0] in ("*", "+") else (x + y <= self.WinRocks)
        if win and h == 3: return True
        if not win and h == 3: return False
        if win and h < 3: return False

        moves = []
        for op in self.Operations:
            moves.append((eval(f"{x}{op}"), y))
            moves.append((x, eval(f"{y}{op}")))

        if h % 2 == 1:
            return all(self.__func_21_correct(m[0], m[1], h+1) for m in moves)
        else:
            return any(self.__func_21_correct(m[0], m[1], h+1) for m in moves)

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EGE Game Solver 19-21")
        self.root.geometry("850x650")
        self.root.configure(bg="#1e293b")  

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        bg_color = "#1e293b"
        card_color = "#334155"
        accent_color = "#6366f1"
        text_color = "#f8fafc"

        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background=card_color, relief="flat")
        
        style.configure("TLabel", background=bg_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground=accent_color)
        style.configure("Subheader.TLabel", font=("Segoe UI", 11, "bold"), background=card_color)
        
        style.configure("TRadiobutton", background=card_color, foreground=text_color, font=("Segoe UI", 10))
        style.configure("TCheckbutton", background=bg_color, foreground=text_color, font=("Segoe UI", 10))

        style.configure("Action.TButton", 
                        background=accent_color, 
                        foreground="white", 
                        font=("Segoe UI", 11, "bold"),
                        padding=10)
        style.map("Action.TButton", background=[('active', '#4f46e5')])

    def create_widgets(self):
        main_layout = ttk.Frame(self.root, padding=20)
        main_layout.pack(fill="both", expand=True)

        header = ttk.Label(main_layout, text="Решатель задач 19-21 ЕГЭ", style="Header.TLabel")
        header.pack(pady=(0, 20))

        content_grid = ttk.Frame(main_layout)
        content_grid.pack(fill="both", expand=True)

        left_col = ttk.Frame(content_grid, padding=(0, 0, 10, 0))
        left_col.pack(side="left", fill="both", expand=True)

        heap_card = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        heap_card.pack(fill="x", pady=(0, 15))

        ttk.Label(heap_card, text="Конфигурация игры", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.task_type = tk.StringVar(value="1")
        modes_frame = ttk.Frame(heap_card, style="Card.TFrame")
        modes_frame.pack(fill="x")
        
        ttk.Radiobutton(modes_frame, text="1 куча", value="1", variable=self.task_type, command=self.toggle_heaps).pack(side="left", padx=10)
        ttk.Radiobutton(modes_frame, text="2 кучи", value="2", variable=self.task_type, command=self.toggle_heaps).pack(side="left", padx=10)

        self.second_heap_frame = ttk.Frame(heap_card, style="Card.TFrame")
        ttk.Label(self.second_heap_frame, text="Камней во 2-й куче:", style="TLabel", background="#334155").pack(side="left", padx=(0, 10))
        self.ent_second_heap = tk.Entry(self.second_heap_frame, width=8, font=("Segoe UI", 11), bg="#1e293b", fg="white", insertbackground="white")
        self.ent_second_heap.pack(side="left")

        params_card = ttk.Frame(left_col, style="Card.TFrame", padding=15)
        params_card.pack(fill="x")

        ttk.Label(params_card, text="Условия победы", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
        
        grid_params = ttk.Frame(params_card, style="Card.TFrame")
        grid_params.pack(fill="x")

        ttk.Label(grid_params, text="Цель (Win):", background="#334155").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_win = tk.Entry(grid_params, width=10, font=("Segoe UI", 11), bg="#1e293b", fg="white", borderwidth=0)
        self.ent_win.grid(row=0, column=1, padx=10, sticky="w")

        ttk.Label(grid_params, text="Лимит (S):", background="#334155").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_s = tk.Entry(grid_params, width=10, font=("Segoe UI", 11), bg="#1e293b", fg="white", borderwidth=0)
        self.ent_s.grid(row=1, column=1, padx=10, sticky="w")

        right_col = ttk.Frame(content_grid, padding=(10, 0, 0, 0))
        right_col.pack(side="left", fill="both", expand=True)

        oper_card = ttk.Frame(right_col, style="Card.TFrame", padding=15)
        oper_card.pack(fill="both", expand=True)

        ttk.Label(oper_card, text="Ходы (напр. +1, *2)", style="Subheader.TLabel").pack(anchor="w", pady=(0, 10))
        
        self.ent_op1 = tk.Entry(oper_card, font=("Segoe UI", 11), bg="#1e293b", fg="white")
        self.ent_op1.pack(fill="x", pady=2)
        self.ent_op2 = tk.Entry(oper_card, font=("Segoe UI", 11), bg="#1e293b", fg="white")
        self.ent_op2.pack(fill="x", pady=2)
        self.ent_op3 = tk.Entry(oper_card, font=("Segoe UI", 11), bg="#1e293b", fg="white")
        self.ent_op3.pack(fill="x", pady=2)

        self.bad_move_var = tk.BooleanVar()
        ttk.Checkbutton(right_col, text="Неудачный ход Пети (зад. 19)", variable=self.bad_move_var).pack(anchor="w", pady=10)

        self.btn_solve = ttk.Button(main_layout, text="РАССЧИТАТЬ ОТВЕТЫ", style="Action.TButton", command=self.solve)
        self.btn_solve.pack(fill="x", pady=20)

        self.results_card = ttk.Frame(main_layout, style="Card.TFrame", padding=15)
        self.results_card.pack(fill="x")
        
        self.lbl_res19 = ttk.Label(self.results_card, text="Задача 19: ---", font=("Segoe UI", 11), background="#334155")
        self.lbl_res19.pack(anchor="w")
        self.lbl_res20 = ttk.Label(self.results_card, text="Задача 20: ---", font=("Segoe UI", 11), background="#334155")
        self.lbl_res20.pack(anchor="w")
        self.lbl_res21 = ttk.Label(self.results_card, text="Задача 21: ---", font=("Segoe UI", 11), background="#334155")
        self.lbl_res21.pack(anchor="w")

    def toggle_heaps(self):
        if self.task_type.get() == "2":
            self.second_heap_frame.pack(fill="x", pady=(10, 0))
        else:
            self.second_heap_frame.pack_forget()

    def solve(self):
        try:
            is_two = self.task_type.get() == "2"
            win_val = int(self.ent_win.get())
            s_val = int(self.ent_s.get())
            
            opers = []
            for e in [self.ent_op1, self.ent_op2, self.ent_op3]:
                val = e.get().strip()
                if val: opers.append(val)

            if not opers: return

            if not is_two:
                solver = Solver_1_Heap()
            else:
                solver = Solver_2_Heap()
                solver.StartRocks = int(self.ent_second_heap.get())

            solver.WinRocks = win_val
            solver.Conditions = s_val
            solver.Operations = opers
            solver.BadMove = self.bad_move_var.get()

            res19 = solver.solve_task_19()
            res20 = solver.solve_task_20()
            res21 = solver.solve_task_21()

            self.lbl_res19.config(text=f"Задача 19 (S): {res19}")
            self.lbl_res20.config(text=f"Задача 20 (S): {res20}")
            self.lbl_res21.config(text=f"Задача 21 (S): {res21}")
            
        except Exception as e:
            self.lbl_res19.config(text="Ошибка: Проверьте ввод данных")
            print(e)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()
