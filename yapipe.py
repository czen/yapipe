# -*- coding: utf8 -*-

from collections import deque


# чтение из файла
def file_reading(input_node):
    with open("in.txt") as f:
        try:
            print("Reading file...", end='')
            i = 1
            for line in f:
                line = line.split('=')
                if line[0] in input_node.ports:
                    input_node.send_data(line[0], line[1][0:-1])
                    # # Выполнение метода do(), если это возможно
                    # portname = []
                    # if input_node.other is not None:
                    #    for i in input_node.get_ports():
                    #        print("_TRACE: ", i, "_")
                    #        if input_node.get_ports().get(i) is not None:
                    #            portname.append(input_node.get_ports().get(i))
                    #     portname.reverse()
                    #     input_node.do(portname.pop(), portname.pop())
            print("Completed")
        except IOError:
            print("FILE ERROR!")


class Operation(object):  # базовый класс
    def __init__(self):
        self.ports = dict()  # Словарь со всеми портами узла
        self.other = None  # Следующий узел
        self.otherPort = deque()  # порт следующего узла, куда передается результат

    # создает очередь <portname>
    def _add_port(self, portname):
        self.ports[portname] = deque()

    # возвращает список портов
    def get_ports(self):
        return self.ports

    def do(self):
        raise

    # добавляет слева значение в очередь <portname>
    def send_data(self, portname, value):
        if portname in self.ports.keys():
            if self.ports[portname] is not None:
                self.ports[portname].append(value)
            else:
                print("NO PORT WITH NAME: ", portname)
        # TODO: проверить, можно ли вызвать do() и сделать это, если можно
        count = 0
        for i in self.ports:
            if len(self.ports[i]) > 0:
                count += 1
            if count == 2:
                count = 0
                self.do()

    # снимает правое (последнее) значение с очереди <portname>
    def get_data(self, portname):
        if portname in self.ports.keys():
            return self.ports[portname].pop()

    # определяет следующий узел графа <other> и его очередь <portname>
    def link(self, other, portname):
        self.other = other
        self.otherPort = portname

    # помещает значение в очередь <portname> следующего узла
    def send_result(self, value):
        if self.other is not None:
            self.other.send_data(self.otherPort, value)


class Sum(Operation):  # обрабатывает событие суммы
    def __init__(self):  # инициализирует объект суммы
        super(Sum, self).__init__()
        self.type = 'SUM'
        self._add_port('term1')
        self._add_port('term2')
        self.term1 = 0
        self.term2 = 0

    def do(self):  # метод суммы
        val = int(self.get_data('term1')) + int(self.get_data('term2'))
        self.send_result(val)


class Mul(Operation):  # обрабатывает событие умножения
    def __init__(self):  # инициализирует объект умножения
        super(Mul, self).__init__()
        self.type = 'MUL'
        self._add_port('multiplier1')
        self._add_port('multiplier2')
        self.multiplier1 = 0
        self.multiplier2 = 0

    def do(self):  # метод умножения
        val = int(self.get_data('multiplier1')) * int(self.get_data('multiplier2'))
        self.send_result(val)


class Concat(Operation):  # обрабатывает событие конкатенации
    def __init__(self):  # инициализирует объект конкатенации
        super(Concat, self).__init__()
        self.type = 'CON'
        self._add_port('string1')
        self._add_port('string2')
        self.string1 = 0
        self.string2 = 0

    def do(self):  # метод конкатенации
        val = str(self.get_data('string1')) + self.get_data('string2')
        self.send_result(val)


class Result(Operation):  # обрабатывает событие завершения процесса
    def __init__(self):  # инициализирует завершающий объект
        super(Result, self).__init__()
        self.type = 'RESULT'
        self._add_port('conclusion')

    def do(self):  # метод вывода результата
        print("CONCLUSION = ", self.ports['conclusion'])


if __name__ == "__main__":
    print()
    sum_node = Sum()
    print("sum_node initialized with operands: ", sum_node.get_ports())
    mul_node = Mul()
    print("mul_node initialized with operands: ", mul_node.get_ports())
    concat_node = Concat()
    print("concat_node initialized with operands: ", concat_node.get_ports())
    result_node = Result()
    print("result_node initialized with operands: ", result_node.get_ports())

    print()
    sum_node.link(mul_node, 'multiplier1')
    mul_node.link(concat_node, 'string1')
    concat_node.link(result_node, 'conclusion')

    file_reading(sum_node)
    file_reading(mul_node)
    file_reading(concat_node)

    # tracing
    print()
    print("sum_node's operands after file_reading: ", sum_node.get_ports())
    print("mul_node's operands after file_reading: ", mul_node.get_ports())
    print("concat_node's operands after file_reading: ", concat_node.get_ports())
    print("result_node's operands after file_reading: ", result_node.get_ports())

    # sum_node.do()
    # mul_node.do()
    # concat_node.do()

    # tracing
    print()
    print("sum_node's operands after DO: ", sum_node.get_ports())
    print("mul_node's operands after DO: ", mul_node.get_ports())
    print("concat_node's operands after DO: ", concat_node.get_ports())
    print("result_node's operands after DO: ", result_node.get_ports())

    print()
    result_node.do()
