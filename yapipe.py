import time
import unittest
from collections import deque


class Operation(object):  # базовый класс
	# список портов (очередь для хранения аргументов)
	# каждый потомок обработает столько аргументов, сколько ему предписано
	ports = {}
	port = deque()  # Очередь данных
	other = None
	otherPort = None

	def sendData(self, portName, value):
		if (portName in self.ports.keys()):
			self.ports[portName].appendleft(value)
		else:
			pass

	def addPort(self, portName):
		self.ports[portName] = deque()

	def getData(self, portName):
		if (portName in self.ports.keys()):
			return self.ports[portName].pop()
		else:
			pass # exception
		# TODO: do() если есть данные


	def Link(self, other, portName):
		self.other = other
		self.otherPort = portName

	def sendResult(self, value):
		self.other.sendData(self.otherPort, value)

# передавать данные между узлами через обьект "дуга", которая будет принимать очередь с результатом последней операции

class Sum(Operation):  # обрабатывает событие суммы
	def __init__(self, a, b):  # инициализирует объект суммы
		self.addPort('A')
		self.addPort('B')
		self.type = 'SUM'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	# поле со списком из двух очередей

	def do(self):  # метод суммы
		try:
			self.res = int(self.operand1) + int(self.operand2)
			self.sendResult(self.res)
			return self.res
		except ValueError:
			print("Wrong data")
		except TypeError:
			print("Wrong Type")


class Mul(Operation):  # обрабатывает событие умножения
	def __init__(self, a, b):  # инициализирует объект умножения
		self.type = 'MUL'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	def do(self):  # метод умножения
		try:
			self.res = int(self.operand1) * int(self.operand2)
			return self.res
		except ValueError:
			print("Wrong data")
		except TypeError:
			print("Wrong Type")


class Concat(Operation):  # обрабатывает событие конкатенации
	def __init__(self, a, b):  # инициализирует объект конкатенации
		self.type = 'CONCAT'
		self.operand1 = a
		self.operand2 = b
		self.res = None

	def do(self):  # метод клнкатенации
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

	def test_operation(self):
		"""Operation test"""
		op = Operation()
		op.addPort('A')
		op.sendData('A', 1)
		val = op.getData('A')
		self.assertEqual(1, val)

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
operation_list = ['+', '*', 'CONCAT', 'concat', 'Concat', 'CON', 'Con', 'con']

# запуск тестов
if __name__ == '__main__':
	unittest.main(exit=False)
	time.sleep(0.2)
print("")

obj = None
A = ''
while True:  # петля
	obj = Operation()
	obj.port.clear()
	operation_set = []

	# Вод операндов
	print("input a queue of arguments (input 'end' to stop):")
	ch = True
	while ch:
		ch = input()
		if ch:
			obj.port.append(ch)
		if ch == "end":
			print("Exiting loop")
			exit()
	print("port = ", obj.port)

	# ввод списка дуг
	print("Input list of operations(input ' ' to stop input)")
	ch = True
	while ch:
		ch = input()
		if ch:
			operation_set.append(ch)
	print("operation_set = ", operation_set)

	# соотнесение ввода к событию
	for i in range(0, len(operation_set)-1):
		meta_operation = operation_set[i]
		if meta_operation in operation_list:

			# Sum
			if meta_operation == '+':
				try:
					s = Sum(obj.port.pop(), obj.port.pop())
					s.do()
					obj.port.append(s.res)
					print("Sum = ", s.res)
				except IndexError:
					print("not enough operands")

			# Mul
			if meta_operation == '*':
				try:
					m = Mul(obj.port.pop(), obj.port.pop())
					m.do()
					obj.port.append(m.res)
					print("Mul = ", m.res)
				except IndexError:
					print("not enough operands")

			# Concat
			if meta_operation == 'CONCAT' or 'concat' or 'Concat' or 'CON' or 'Con' or 'con':
				try:
					c = Concat(obj.port.pop(), obj.port.pop())
					c.do()
					obj.port.append(c.res)
					print("Concat = ", c.res)
				except IndexError:
					print("not enough operands")

		else:
			print("UNKNOWN OPERATION")

	print("")
	print("port = ", obj.port)

	# f = True
	# operation_set = []
	# # Первый ввод начальных данных
	# while f:
	# 	A = input("input A or press ↲ for result in last event ('end' to stop): ")
	# 	if (obj is not None) and (A == ''):
	# 		A = obj.res
	# 		print("input A: ", A)
	# 	if A != '':
	# 		f = False
	# if A == 'end':
	# 	break
	# B = input("input B: ")
	#
	# # ввод списка дуг через перечисление операций
	# print("Input list of operations(input ' ' to stop input)")
	# c = True
	# while c:
	# 	c = input()
	# 	if c:
	# 		operation_set.append(c)
	# print(operation_set)
	#
	# # данные для классификации события
	# for i in range(0, len(operation_set)):
	# 	meta_operation = operation_set[i]
	# 	if meta_operation in operation_list:  # соотнесение ввода к событию
	# 		if i != 0:
	# 			print("Input operand for next operation")
	# 			A = input()
	# 		if meta_operation == '+':  # Sum
	# 			obj = Sum(A, B)
	# 			print("Sum = ", obj.do())
	# 			B = obj.res
	# 		elif meta_operation == '*':  # Mul
	# 			obj = Mul(A, B)
	# 			print("Mul = ", obj.do())
	# 			B = obj.res
	# 		elif meta_operation == 'CONCAT' or 'concat' or 'Concat' or 'CON' or 'Con' or 'con':  # Concat
	# 			obj = Concat(A, B)
	# 			print("Concat = ", obj.do())
	# 			B = obj.res
	# 	else:
	# 		print("UNKNOWN OPERATION")

	for j in range(8):  # следующая итерация
		print('*', end=' ', flush=True)
		time.sleep(0.1)
	print("")

