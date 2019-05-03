import time
from collections import deque

class Operation(object):  # базовый класс
	# список портов (очередь для хранения аргументов)
	# каждый потомок обработает столько аргументов, сколько ему предписано
	ports = {}
	port = deque()  # Очередь данных

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
			pass

# передавать данные между узлами через обьект "дуга", которая будет принимать очередь с результатом последней операции

class Sum(Operation):  # обрабатывает событие суммы
	def __init__(self, a, b):  # инициализирует объект суммы
		self.type = 'SUM'
		self.operand1 = a
		self.operand2 = b
		self.res = None


	# поле со списком из двух очередей

	def do(self):  # метод суммы
		try:
			self.res = int(self.operand1) + int(self.operand2)
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

# список с метками операций
operation_list = ['+', '*', 'CONCAT', 'concat', 'Concat', 'CON', 'Con', 'con']

if __name__ == '__main__':
	time.sleep(0.2)
	print("")
	obj = None
	A = ''
	while True:  # Цикл
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

