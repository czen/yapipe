import time


class Event(object):  # базовый класс
	pass


class Sum(Event):  # обрабатывает событие суммы
	def __init__(self, a, b):  # инициализирует объект суммы
		self.type = 'SUM'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	def do(self):  # метод суммы
		try:
			self.res = int(self.operand1) + int(self.operand2)
			return self.res
		except ValueError:
			print("Wrong data")
		except TypeError:
			print("Wrong Type")


class Mul(Event):  # обрабатывает событие умножения
	def __init__(self, a, b):  # инициализирует объект умножения
		self.type = 'MUL'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	def do(self):  # метод суммы
		try:
			self.res = int(self.operand1) + int(self.operand2)
			return self.res
		except ValueError:
			print("Wrong data")
		except TypeError:
			print("Wrong Type")


class Concat(Event):  # обрабатывает событие конкатениции
	def __init__(self, a, b):  # инициализирует объект конкатениции
		self.type = 'CONCAT'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	def do(self):  # метод суммы
		try:
			self.res = str(self.operand1) + self.operand2
			return self.res
		except ValueError:
			print("Wrong Value")
		except TypeError:
			print("Wrong Type")


operation_list = ['+', '*', 'CONCAT']

obj = None
while True:  # петля
	f = True
	while f:
		A = input("input A or press ↲ for result in previous event: ")
		if (obj is not None) & (A == ''):
				A = obj.res
				print("input A: ", A)
		if A != '':
			f = False
	if A == 'end':
		break
	B = input("input B: ")

	meta_operation = input("input Operation: ")  # данные для классификации события

	if meta_operation in operation_list:  # соотнесение ввода к событию
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

for j in range(8):  # следующая итерация
	print('*', end=' ')
	time.sleep(0.2)

print("Exiting loop")
