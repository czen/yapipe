import time


class Event(object):  # базовый класс
    pass


class Sum(Event):  # обрабатывает событие суммы
    def __init__(self, a, b):  # инициализирует объект суммы
        self.type = 'SUM'
        self.operand1 = a
        self.operand2 = b

    def do(self):  # метод суммы
        res = int(self.operand1) + int(self.operand2)
        return res


class Mul(Event):  # обрабатывает событие умножения
    def __init__(self, a, b):  # инициализирует объект умножения
        self.type = 'MUL'
        self.operand1 = a
        self.operand2 = b

    def do(self):  # метод умножения
        res = int(self.operand1) * int(self.operand2)
        return res


class Concat(Event):  # обрабатывает событие конкатениции
    def __init__(self, a, b):  # инициализирует объект конкатениции
        self.type = 'CONCAT'
        self.operand1 = a
        self.operand2 = b

    def do(self):  # метод конкатенации
        res = self.operand1 + self.operand2
        return res


# operation_list = {'+': Sum(), '*': Mul(), 'CONCAT': Concat()}
operation_list = ['+', '*', 'CONCAT']

"""
q1 = queue.Queue()
q2 = queue.Queue()
"""

while True:  # петля
    print("input A")
    A = input()
    if A == 'end':
        break
    print("input B")
    B = input()
    print("input Operation")
    meta_operation = input()  # данные для классификации события

    # if meta_operation in operation_list.keys():
    # work = operation_list(meta_operation)

    """ !!! РЕАЛИЗОВАТЬ СЛОВАРЬ !!!  """
    if meta_operation in operation_list:
        if meta_operation == '+':
            obj = Sum(A, B)
            print("Sum = ", obj.do())

        elif meta_operation == '*':
            obj = Mul(A, B)
            print("Mul = ", obj.do())

        elif meta_operation == 'CONCAT':
            obj = Concat(A, B)
            print("Concat = ", obj.do())
        else:
            print("UNKNOWN OPERATION")
    print("********")
    time.sleep(2)  # следующая итерация
print("Exiting loop")
