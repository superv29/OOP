from tkinter import *
from abc import *
import threading

class Solver(ABC):
    def __init__(self):
        self._win_rocks = NONE
        self._operations = NONE
        self._type = NONE
        self._conditions = NONE
        self._bad_move = NONE

    def __set_win_rocks(self, count):
        self._win_rocks = count
    
    def __set_operations(self, operations):
        self._operations = operations

    def __set_type(self, type):
        self._type = type
    
    def __set_conditions(self, cond):
        self._conditions = cond

    def __set_bad_move(self, flag):
        self._bad_move = flag

    WinRocks = property(lambda x: x._win_rocks, __set_win_rocks)
    Operations = property(lambda x: x._operations, __set_operations)
    Type = property(lambda x: x._type, __set_type)
    Conditions = property(lambda x: x._conditions, __set_conditions)
    BadMove = property(lambda x: x._bad_move, __set_bad_move)

    @abstractmethod
    def solve_task_19(self):
        pass

    @abstractmethod
    def solve_task_20(self):
        pass

    @abstractmethod
    def solve_task_21(self):
        pass

class Solver_1_Heap(Solver):
    def __init__(self):
        super().__init__()
        self._type = "1"

    def solve_task_19(self):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_19(s, 1):
                    return s
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_19(s, 1):
                    return s
                
    def solve_task_20(self):
        answers = []
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_20(s, 1):
                    answers.append(s)
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_20(s, 1):
                    answers.append(s)
        return answers
    
    def solve_task_21(self):
        temps = []
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_21(s, 1):
                    temps.append(s)
            for s in range(1, self.Conditions):
                if self.__func_21_correct(s, 1):
                    for i in range(len(temps)):
                        if temps[i] == s:
                            temps.remove(s)
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_21(s, 1):
                    temps.append(s)
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_21_correct(s, 1):
                    for i in range(len(temps)):
                        if temps[i] == s:
                            temps.remove(s)
        return temps[0]

    def __func_19(self, x, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x >= self.WinRocks and h == 3: return True
            if x < self.WinRocks and h == 3: return False
            if x >= self.WinRocks: return False
        else:
            if x <= self.WinRocks and h == 3: return True
            if x > self.WinRocks and h == 3: return False
            if x <= self.WinRocks: return False 

        if len(self.Operations) == 2:
            if self.BadMove != True:
                if h%2 == 1:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) and self.__func_19(eval(f"x{self.Operations[1]}"), h+1)
                else:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), h+1)
            else:
                return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if self.BadMove != True:
                if h%2 == 1:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) and self.__func_19(eval(f"x{self.Operations[1]}"), h+1) and self.__func_19(eval(f"x{self.Operations[2]}"), h+1)
                else:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), h+1) or self.__func_19(eval(f"x{self.Operations[2]}"), h+1)
            else:
                return self.__func_19(eval(f"x{self.Operations[0]}"), h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), h+1) or self.__func_19(eval(f"x{self.Operations[2]}"), h+1)
    
    def __func_20(self, x, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x >= self.WinRocks and h == 4: return True
            if x < self.WinRocks and h == 4: return False
            if x >= self.WinRocks: return False
        else:
            if x <= self.WinRocks and h == 4: return True
            if x > self.WinRocks and h == 4: return False
            if x <= self.WinRocks: return False 

        if len(self.Operations) == 2:
            if h%2 == 0:
                return self.__func_20(eval(f"x{self.Operations[0]}"), h+1) and self.__func_20(eval(f"x{self.Operations[1]}"), h+1)
            else:
                return self.__func_20(eval(f"x{self.Operations[0]}"), h+1) or self.__func_20(eval(f"x{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if h%2 == 0:
                return self.__func_20(eval(f"x{self.Operations[0]}"), h+1) and self.__func_20(eval(f"x{self.Operations[1]}"), h+1) and self.__func_20(eval(f"x{self.Operations[2]}"), h+1)
            else:
                return self.__func_20(eval(f"x{self.Operations[0]}"), h+1) or self.__func_20(eval(f"x{self.Operations[1]}"), h+1) or self.__func_20(eval(f"x{self.Operations[2]}"), h+1)

    def __func_21(self, x, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x >= self.WinRocks and (h == 3 or h == 5): return True
            if x < self.WinRocks and h == 5: return False
            if x >= self.WinRocks and h < 5: return False
        else:
            if x <= self.WinRocks and (h == 3 or h == 5): return True
            if x > self.WinRocks and h == 5: return False
            if x <= self.WinRocks and h < 5: return False 

        if len(self.Operations) == 2:
            if h%2 == 1:
                return self.__func_21(eval(f"x{self.Operations[0]}"), h+1) and self.__func_21(eval(f"x{self.Operations[1]}"), h+1)
            else:
                return self.__func_21(eval(f"x{self.Operations[0]}"), h+1) or self.__func_21(eval(f"x{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if h%2 == 1:
                return self.__func_21(eval(f"x{self.Operations[0]}"), h+1) and self.__func_21(eval(f"x{self.Operations[1]}"), h+1) and self.__func_21(eval(f"x{self.Operations[2]}"), h+1)
            else:
                return self.__func_21(eval(f"x{self.Operations[0]}"), h+1) or self.__func_21(eval(f"x{self.Operations[1]}"), h+1) or self.__func_21(eval(f"x{self.Operations[2]}"), h+1)

    def __func_21_correct(self, x, h):
            if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
                if x >= self.WinRocks and h == 3: return True
                if x < self.WinRocks and h == 3: return False
                if x >= self.WinRocks and h < 3: return False
            else:
                if x <= self.WinRocks and h == 3: return True
                if x > self.WinRocks and h == 3: return False
                if x <= self.WinRocks and h < 3: return False 
            if len(self.Operations) == 2:
                if h%2 == 1:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), h+1) and self.__func_21_correct(eval(f"x{self.Operations[1]}"), h+1)
                else:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), h+1) or self.__func_21_correct(eval(f"x{self.Operations[1]}"), h+1)
            elif len(self.Operations) == 3:
                if h%2 == 1:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), h+1) and self.__func_21_correct(eval(f"x{self.Operations[1]}"), h+1) and self.__func_21_correct(eval(f"x{self.Operations[2]}"), h+1)
                else:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), h+1) or self.__func_21_correct(eval(f"x{self.Operations[1]}"), h+1) or self.__func_21_correct(eval(f"x{self.Operations[2]}"), h+1)

class Solver_2_Heap(Solver):
    def __init__(self):
        super().__init__()
        self._type = "2"
        self._start_rocks = NONE
    
    def __set_start_rocks(self, start):
        self._start_rocks = start

    StartRocks = property(lambda x: x._start_rocks, __set_start_rocks)

    def solve_task_19(self):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_19(s, self.StartRocks, 1):
                    return s
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_19(s, self.StartRocks, 1):
                    return s

    def solve_task_20(self):
        answers = []
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_20(s, self.StartRocks, 1):
                    answers.append(s)
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_20(s, self.StartRocks, 1):
                    answers.append(s)
        return answers

    def solve_task_21(self):
        temps = []
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            for s in range(1, self.Conditions):
                if self.__func_21(s, self.StartRocks, 1):
                    temps.append(s)
            for s in range(1, self.Conditions):
                if self.__func_21_correct(s, self.StartRocks, 1):
                    for i in range(len(temps)):
                        if temps[i] == s:
                            temps.remove(s)
        else:
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_21(s, self.StartRocks, 1):
                    temps.append(s)
            for s in range(self.Conditions, self.Conditions*1000):
                if self.__func_21_correct(s, self.StartRocks, 1):
                    for i in range(len(temps)):
                        if temps[i] == s:
                            temps.remove(s)
        return temps[0]

    def __func_19(self, x, y, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x + y >= self.WinRocks and h == 3: return True
            if x + y < self.WinRocks and h == 3: return False
            if x + y >= self.WinRocks: return False
        else:
            if x + y <= self.WinRocks and h == 3: return True
            if x + y > self.WinRocks and h == 3: return False
            if x + y <= self.WinRocks: return False 
 
        if len(self.Operations) == 2:
            if self.BadMove != True:
                if h%2 == 1:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) and self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1)
                else:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                        or self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) or self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1)
            else:
                return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                    or self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) or self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if self.BadMove != True:
                if h%2 == 1:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_19(eval(f"x{self.Operations[2]}"), y, h+1) and self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) \
                            and self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1) and self.__func_19(x, eval(f"y{self.Operations[2]}"), h+1)
                else:
                    return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                        or self.__func_19(eval(f"x{self.Operations[2]}"), y, h+1) or self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) \
                            or self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1) or self.__func_19(x, eval(f"y{self.Operations[2]}"), h+1)
            else:
                return self.__func_19(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_19(eval(f"x{self.Operations[1]}"), y, h+1) \
                    or self.__func_19(eval(f"x{self.Operations[2]}"), y, h+1) or self.__func_19(x, eval(f"y{self.Operations[0]}"), h+1) \
                        or self.__func_19(x, eval(f"y{self.Operations[1]}"), h+1) or self.__func_19(x, eval(f"y{self.Operations[2]}"), h+1)
   
    def __func_20(self, x, y, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x + y >= self.WinRocks and h == 4: return True
            if x + y < self.WinRocks and h == 4: return False
            if x + y >= self.WinRocks: return False
        else:
            if x + y <= self.WinRocks and h == 4: return True
            if x + y > self.WinRocks and h == 4: return False
            if x + y <= self.WinRocks: return False 

        if len(self.Operations) == 2:
            if h%2 == 0:
                return self.__func_20(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_20(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_20(x, eval(f"y{self.Operations[0]}"), h+1) and self.__func_20(x, eval(f"y{self.Operations[1]}"), h+1)
            else:
                return self.__func_20(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_20(eval(f"x{self.Operations[1]}"), y, h+1) \
                        or self.__func_20(x, eval(f"y{self.Operations[0]}"), h+1) or self.__func_20(x, eval(f"y{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if h%2 == 0:
                return self.__func_20(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_20(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_20(eval(f"x{self.Operations[2]}"), y, h+1) and self.__func_20(x, eval(f"y{self.Operations[0]}"), h+1) \
                            and self.__func_20(x, eval(f"y{self.Operations[1]}"), h+1) and self.__func_20(x, eval(f"y{self.Operations[2]}"), h+1)
            else:
                return self.__func_20(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_20(eval(f"x{self.Operations[1]}"), y, h+1) \
                    or self.__func_20(eval(f"x{self.Operations[2]}"), y, h+1) or self.__func_20(x, eval(f"y{self.Operations[0]}"), h+1) \
                        or self.__func_20(x, eval(f"y{self.Operations[1]}"), h+1) or self.__func_20(x, eval(f"y{self.Operations[2]}"), h+1)

    def __func_21(self, x, y, h):
        if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
            if x + y >= self.WinRocks and (h == 3 or h == 5): return True
            if x + y < self.WinRocks and h == 5: return False
            if x + y >= self.WinRocks and h < 5: return False
        else:
            if x + y <= self.WinRocks and (h == 3 or h == 5): return True
            if x + y > self.WinRocks and h == 5: return False
            if x + y <= self.WinRocks and h < 5: return False 

        if len(self.Operations) == 2:
            if h%2 == 1:
                return self.__func_21(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_21(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_21(x, eval(f"y{self.Operations[0]}"), h+1) and self.__func_21(x, eval(f"y{self.Operations[1]}"), h+1)
            else:
                return self.__func_21(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_21(eval(f"x{self.Operations[1]}"), y, h+1) \
                        or self.__func_21(x, eval(f"y{self.Operations[0]}"), h+1) or self.__func_21(x, eval(f"y{self.Operations[1]}"), h+1)
        elif len(self.Operations) == 3:
            if h%2 == 1:
                return self.__func_21(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_21(eval(f"x{self.Operations[1]}"), y, h+1) \
                        and self.__func_21(eval(f"x{self.Operations[2]}"), y, h+1) and self.__func_21(x, eval(f"y{self.Operations[0]}"), h+1) \
                            and self.__func_21(x, eval(f"y{self.Operations[1]}"), h+1) and self.__func_21(x, eval(f"y{self.Operations[2]}"), h+1)
            else:
                return self.__func_21(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_21(eval(f"x{self.Operations[1]}"), y, h+1) \
                    or self.__func_21(eval(f"x{self.Operations[2]}"), y, h+1) or self.__func_21(x, eval(f"y{self.Operations[0]}"), h+1) \
                        or self.__func_21(x, eval(f"y{self.Operations[1]}"), h+1) or self.__func_21(x, eval(f"y{self.Operations[2]}"), h+1)
    
    def __func_21_correct(self, x, y, h):
            if self.Operations[0][0] == "*" or self.Operations[0][0] == "+":
                if x + y >= self.WinRocks and h == 3: return True
                if x + y < self.WinRocks and h == 3: return False
                if x + y >= self.WinRocks and h < 3: return False
            else:
                if x + y <= self.WinRocks and h == 3: return True
                if x + y > self.WinRocks and h == 3: return False
                if x + y <= self.WinRocks and h < 3: return False 
            if len(self.Operations) == 2:
                if h%2 == 1:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_21_correct(eval(f"x{self.Operations[1]}"), y, h+1) \
                            and self.__func_21_correct(x, eval(f"y{self.Operations[0]}"), h+1) and self.__func_21_correct(x, eval(f"y{self.Operations[1]}"), h+1)
                else:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_21_correct(eval(f"x{self.Operations[1]}"), y, h+1) \
                            or self.__func_21_correct(x, eval(f"y{self.Operations[0]}"), h+1) or self.__func_21_correct(x, eval(f"y{self.Operations[1]}"), h+1)
            elif len(self.Operations) == 3:
                if h%2 == 1:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), y, h+1) and self.__func_21_correct(eval(f"x{self.Operations[1]}"), y, h+1) \
                            and self.__func_21_correct(eval(f"x{self.Operations[2]}"), y, h+1) and self.__func_21_correct(x, eval(f"y{self.Operations[0]}"), h+1) \
                                and self.__func_21_correct(x, eval(f"y{self.Operations[1]}"), h+1) and self.__func_21_correct(x, eval(f"y{self.Operations[2]}"), h+1)
                else:
                    return self.__func_21_correct(eval(f"x{self.Operations[0]}"), y, h+1) or self.__func_21_correct(eval(f"x{self.Operations[1]}"), y, h+1) \
                        or self.__func_21_correct(eval(f"x{self.Operations[2]}"), y, h+1) or self.__func_21_correct(x, eval(f"y{self.Operations[0]}"), h+1) \
                            or self.__func_21_correct(x, eval(f"y{self.Operations[1]}"), h+1) or self.__func_21_correct(x, eval(f"y{self.Operations[2]}"), h+1) 

root = Tk()
root.title("Solver 19-21 EGE")
root.geometry("720x510")
root.configure(bg="white")

frame_conditions = Frame(root, bg="white")
frame_conditions.pack(fill=X, padx=20, pady=10)

header_main = Label(root, text="Задания 19-21 ЕГЭ", font=("Arial", 14, "bold"), bg="white", fg="black")
header_main.pack(anchor=CENTER, pady=10)

main_container = Frame(frame_conditions, bg="white")
main_container.pack(fill=X, pady=10)

left_frame = Frame(main_container, bg="white")
left_frame.pack(side=LEFT, anchor=N, padx=(0, 20))

header_type = Label(left_frame, text="Выберите количество куч", font=("Arial", 10), bg="white", fg="black")
header_type.pack(anchor=W)

task_1 = "1 куча"
task_2 = "2 кучи"
task_type = StringVar(value=task_1)

second_heap_label = None
second_heap_entry = None

def on_task_type_change(*args):
    global second_heap_label, second_heap_entry
    
    if task_type.get() == task_2:
        if second_heap_label is None:
            second_heap_label = Label(left_frame, text="Введите начальное количество камней во 2-й куче", 
                                     font=("Arial", 9), bg="white", fg="black")
            second_heap_label.pack(anchor=W, pady=(10, 2))
            
            second_heap_entry = Entry(left_frame, font=("Arial", 10), width=8, fg="black")
            second_heap_entry.pack(anchor=W, pady=5)
    else:
        if second_heap_label is not None:
            second_heap_label.destroy()
            second_heap_entry.destroy()
            second_heap_label = None
            second_heap_entry = None

task_type.trace('w', on_task_type_change)

task1_btn = Radiobutton(left_frame, text=task_1, value=task_1, variable=task_type,
                       bg="white", fg="black", selectcolor="white", command=on_task_type_change)
task1_btn.pack(anchor=W, pady=2)
  
task2_btn = Radiobutton(left_frame, text=task_2, value=task_2, variable=task_type,
                       bg="white", fg="black", selectcolor="white", command=on_task_type_change)
task2_btn.pack(anchor=W, pady=2)

header_win = Label(left_frame, text="Введите необходимое количество камней из условия", 
                  font=("Arial", 9), bg="white", fg="black")
header_win.pack(anchor=W, pady=(10, 0))

win_rocks = Entry(left_frame, font=("Arial", 10), width=8, fg="black")
win_rocks.pack(anchor=W, pady=5)

header_limit = Label(left_frame, text="Введите максимальный размер кучи (S)", 
                    font=("Arial", 9), bg="white", fg="black")
header_limit.pack(anchor=W, pady=(10, 0))

heap_limit_entry = Entry(left_frame, font=("Arial", 10), width=8, fg="black")
heap_limit_entry.pack(anchor=W, pady=5)

right_frame = Frame(main_container, bg="white")
right_frame.pack(side=LEFT, anchor=N)

header_oper = Label(right_frame, text="Введите возможные операции (например //2)", 
                   font=("Arial", 10), bg="white", fg="black")
header_oper.pack(anchor=W)

oper1 = Entry(right_frame, font=("Arial", 10), width=8, fg="black")
oper1.pack(anchor=W, pady=5)
oper2 = Entry(right_frame, font=("Arial", 10), width=8, fg="black")
oper2.pack(anchor=W, pady=5)
oper3 = Entry(right_frame, font=("Arial", 10), width=8, fg="black")
oper3.pack(anchor=W, pady=5)

bad_move_var = BooleanVar()
bad_move_checkbox = Checkbutton(
    right_frame, 
    text="Неудачный ход Пети (для 19 задачи)", 
    variable=bad_move_var,
    bg="white", fg="black", selectcolor="white"
)
bad_move_checkbox.pack(anchor=W, pady=(10, 0))

solve_button = Button(root, text="Решить", font=("Arial", 11, "bold"), 
                     bg="lightblue", fg="black", command=lambda: show_answers())
solve_button.pack(pady=10)

answers_frame = None
answers_label = None
answer_labels = []
solver = NONE

def show_answers():
    global answers_frame, answers_label, answer_labels
    
    if answers_frame is not None:
        answers_frame.destroy()
    
    answers_frame = Frame(root, bg="white")
    answers_frame.pack(fill=X, padx=20, pady=10)
    
    answers_label = Label(answers_frame, text="Ответы:", font=("Arial", 12, "bold"), 
                         bg="white", fg="black")
    answers_label.pack(anchor=W, pady=(0, 10))

    answer_labels.clear()
    
    answers_texts = [
        "Ответ 19: ...",
        "Ответ 20: ...", 
        "Ответ 21: ..."
    ]
    
    for i, text in enumerate(answers_texts):
        answer_label = Label(answers_frame, text=text, font=("Arial", 10), 
                           bg="white", fg="black")
        answer_label.pack(anchor=W, pady=2)
        answer_labels.append(answer_label)
    
    try:
        if get_type() == "1":
            solver = Solver_1_Heap()
        else:
            solver = Solver_2_Heap()
            solver.StartRocks = int(get_second_heap())

        solver.WinRocks = int(get_win_rocks())
        solver.Conditions = int(get_heap_size())
        solver.Operations = get_operetions()
        solver.BadMove = get_flag_bad_move()
        task_19 = solver.solve_task_19()
        task_20 = solver.solve_task_20()
        task_21 = solver.solve_task_21()
        calculate_answers(task_19, task_20, task_21)
    except Exception as e:
        for i, label in enumerate(answer_labels):
            if i == 0:
                label.config(text="Ошибка: Проверьте ввод данных")

def get_type():
    global task_type, task_1
    if task_type.get() == task_1:
        return "1"
    else:
        return "2"
    
def get_win_rocks():
    global win_rocks
    return win_rocks.get()

def get_heap_size():
    global heap_limit_entry
    return heap_limit_entry.get()

def get_second_heap():
    global second_heap_entry
    return second_heap_entry.get()

def get_operetions():
    global oper1, oper2, oper3
    opers = []
    if oper1.get() != "":
        opers.append(oper1.get().strip())
    if oper2.get() != "":
        opers.append(oper2.get().strip())
    if oper3.get() != "":
        opers.append(oper3.get().strip())
    return opers
    
def get_flag_bad_move():
    global bad_move_var
    return bad_move_var.get()

def calculate_answers(task_19, task_20, task_21):
    if answers_frame is not None:
        task_20_str = ", ".join(str(x) for x in task_20) if isinstance(task_20, list) else str(task_20)
        answers = [
            f"Ответ 19: {task_19}",
            f"Ответ 20: {task_20_str}", 
            f"Ответ 21: {task_21}"
        ]
        for i, label in enumerate(answer_labels):
            label.config(text=answers[i])

root.mainloop()
