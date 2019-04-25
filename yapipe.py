import time
import unittest


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
			self.res = int(self.operand1) * int(self.operand2)
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
			self.res = str(self.operand1) + str(self.operand2)
			return self.res
		except ValueError:
			print("Wrong Value")
		except TypeError:
			print("Wrong Type")


class YapipeTest(unittest.TestCase):
	"""yapipe tests"""

	@classmethod
	def tearDownClass(cls):
		"""Tear down for class"""
		print("==========")
		print("tearDownClass")

	def setUp(self):
		"""Set up for test"""
		print("Set up for [" + self.shortDescription() + "]")

	def tearDown(self):
		"""Tear down for test"""
		print("Tear down for [" + self.shortDescription() + "]")
		print("")

	def test_sum(self):
		"""Sum test"""
		print("id: " + self.id())
		testobj = Sum(1, 2)
		testobj.do()
		self.assertEqual(3, testobj.res)

	def test_mul(self):
		"""Mul test"""
		print("id: " + self.id())
		testobj = Mul(1, 3)
		testobj.do()
		self.assertEqual(3, testobj.res)

	def test_concat(self):
		"""Concat test"""
		print("id: " + self.id())
		testobj = Concat('ya', 'pipe')
		testobj.do()
		self.assertEqual('yapipe', testobj.res)


# список с метками операций
operation_list = ['+', '*', 'CONCAT', 'concat', 'Concat','CON', 'Con', 'con']

# запуск тестов
if __name__ == '__main__':
	unittest.main(exit=False)
	time.sleep(0.1)
print("")


obj = None
A = ''
while True:  # петля
	f = True
	operation_set = []
	# Первый ввод начальных данных
	while f:
		A = input("input A or press ↲ for result in last event ('end' to stop): ")
		if (obj is not None) and (A == ''):
			A = obj.res
			print("input A: ", A)
		if A != '':
			f = False
	if A == 'end':
		break
	B = input("input B: ")

	# ввод списка дуг через перечисление операций
	print("Input list of operations(input ' ' to stop input)")
	c = True
	while c:
		c = input()
		if c:
			operation_set.append(c)
	print(operation_set)

	# данные для классификации события
	for i in range(0, len(operation_set)):
		meta_operation = operation_set[i]
		if meta_operation in operation_list:  # соотнесение ввода к событию
			if i != 0:
				print("Input operand for next operation")
				A = input()
			if meta_operation == '+':  # Sum
				obj = Sum(A, B)
				print("Sum = ", obj.do())
				B = obj.res
			elif meta_operation == '*':  # Mul
				obj = Mul(A, B)
				print("Mul = ", obj.do())
				B = obj.res
			elif meta_operation == 'CONCAT' or 'concat' or 'Concat' or 'CON' or 'Con' or 'con':  # Concat
				obj = Concat(A, B)
				print("Concat = ", obj.do())
				B = obj.res
		else:
			print("UNKNOWN OPERATION")

	for j in range(8):  # следующая итерация
		print('*', end=' ', flush=True)
		time.sleep(0.1)
	print("")
	print("Exiting loop")
	print("")
