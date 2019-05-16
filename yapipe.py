import time
from collections import deque

class Operation(object):  # базовый класс
	# список портов (очередь для хранения аргументов)
	# каждый потомок обработает столько аргументов, сколько ему предписано
	ports = {}  # Список портов (очередей данных)
	port = deque()  # Очередь данных
	other = None
	otherPort = deque()

	# создает очередь <portname>
	def add_port(self, portname):
		self.ports[portname] = deque()

	# возвращает список портов
	def get_ports(self):
		return self.ports

	# добавляет слева значение в очередь <portname>
	def send_data(self, portname, value):
		if portname in self.ports.keys():
			self.ports[portname].appendleft(value)
		else:
			pass

	# снимает правое (последнее) значение с очереди <portname>
	def get_data(self, portname):
		if portname in self.ports.keys():
			return self.ports[portname].pop()
		else:
			pass  # exception

	# TODO: do() если есть данные

	# определяет следующий узел графа <other> и его очередь <portname>
	def link(self, other, portname):
		self.other = other
		self.otherPort = portname

	# помещает значение в очередь <portname> следующего узла
	def send_result(self, value):
		self.other.send_data(self.otherPort, value)


# передавать данные между узлами через обьект "дуга", которая будет принимать очередь с результатом последней операции


class Sum(Operation):  # обрабатывает событие суммы
	def __init__(self):  # инициализирует объект суммы
		self.type = 'SUM'
		self.add_port('A')
		self.add_port('B')
		self.operand1 = 0
		self.operand2 = 0
		self.res = None

	# поле со списком из двух очередей

	def do(self, portname1, portname2):  # метод суммы
		operand1 = self.get_data(portname1)
		operand2 = self.get_data(portname2)
		val = operand1 + operand2
		self.send_result(val)


class Mul(Operation):  # обрабатывает событие умножения
	def __init__(self):  # инициализирует объект умножения
		self.type = 'MUL'
		self.add_port('A')
		self.add_port('B')
		self.operand1 = 0
		self.operand2 = 0
		self.res = None

	def do(self, portname1, portname2):  # метод умножения
		operand1 = self.get_data(portname1)
		operand2 = self.get_data(portname2)
		val = operand1 * operand2
		self.send_result(val)


class Concat(Operation):  # обрабатывает событие конкатенации
	def __init__(self):  # инициализирует объект конкатенации
		self.type = 'CON'
		self.add_port('A')
		self.add_port('B')
		self.operand1 = 0
		self.operand2 = 0
		self.res = None

	def do(self, portname1, portname2):  # метод клнкатенации
		operand1 = self.get_data(portname1)
		operand2 = self.get_data(portname2)
		val = str(operand1) + str(operand2)
		self.send_result(val)

# список с символами операций
operation_list = ['+', '*', 'CONCAT', 'concat', 'Concat', 'CON', 'Con', 'con']

if __name__ == '__main__':
	time.sleep(0.5)
	print("")
    # obj = None
	# A = ''
	while True:  # цикл ввода и действий
		print("getting started")
		print("input the operation(node)")

		meta_operation = input()  # получение очередной операции
		if meta_operation == 'end':
			break

		# создание узла, соответствующего операции
		if meta_operation in operation_list:
			# Sum
			if meta_operation == '+':
				obj_first = Sum()

			# Mul
			if meta_operation == '*':
				obj_first = Mul()

			# Concat
			if meta_operation == 'CONCAT' or 'concat' or 'Concat' or 'CON' or 'Con' or 'con':
				obj_first = Concat()
		else:
			print("UNKNOWN OPERATION")
		print("Object constructed")

		# чтение из файла
		with open("in.txt") as f:
			for line in f:
				line = line.split()
				try:
					if line[0] not in obj_first.ports.keys():
						raise Exception("port doesn't exist")
					for i in range(1, len(line)):
						obj_first.send_data(line[0], line[i])
						print(line[i], " is added to ", line[0])
				except (AttributeError, Exception):
					pass

		"""
	  print("input next nods")
	  print("Input list of operations(input ' ' to stop input)")
	  operation_set = []
	  ch = True
	  while ch:
		ch = input()
		if ch:
		  operation_set.append(ch)
	  print("operation_set = ", operation_set)
	  """
		# obj = Operation()
		# obj.port.clear()
		# operation_set = []
		#
		# # Вод операндов
		# print("input a queue of arguments (input 'end' to stop):")
		# ch = True
		# while ch:
		# 	ch = input()
		# 	if ch:
		# 		obj.port.append(ch)
		# 	if ch == "end":
		# 		print("Exiting loop")
		# 		exit()
		# print("port = ", obj.port)
		#
		# # ввод списка дуг
		# print("Input list of operations(input ' ' to stop input)")
		# ch = True
		# while ch:
		# 	ch = input()
		# 	if ch:
		# 		operation_set.append(ch)
		# print("operation_set = ", operation_set)
		#
		# # соотнесение ввода к событию
		# for i in range(0, len(operation_set) - 1):
		# 	meta_operation = operation_set[i]
		# 	if meta_operation in operation_list:
		#
		# 		# Sum
		# 		if meta_operation == '+':
		# 			try:
		# 				s = Sum(obj.port.pop(), obj.port.pop())
		# 				s.do()
		# 				obj.port.append(s.res)
		# 				print("Sum = ", s.res)
		# 			except IndexError:
		# 				print("not enough operands")
		#
		# 		# Mul
		# 		if meta_operation == '*':
		# 			try:
		# 				m = Mul(obj.port.pop(), obj.port.pop())
		# 				m.do()
		# 				obj.port.append(m.res)
		# 				print("Mul = ", m.res)
		# 			except IndexError:
		# 				print("not enough operands")
		#
		# 		# Concat
		# 		if meta_operation == 'CONCAT' or 'concat' or 'Concat' or 'CON' or 'Con' or 'con':
		# 			try:
		# 				c = Concat(obj.port.pop(), obj.port.pop())
		# 				c.do()
		# 				obj.port.append(c.res)
		# 				print("Concat = ", c.res)
		# 			except IndexError:
		# 				print("not enough operands")
		#
		# 	else:
		# 		print("UNKNOWN OPERATION")
		#
		# print("")
		# print("port = ", obj.port)

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
