# -*- coding: utf8 -*-

from collections import deque


# чтение из файла
def file_reading():
    with open("in.txt") as f:
        try:
            print("Reading file...", end='')
            for line in f:
                line = line.split('=')
                if line[0] in port_map:
                    port_map[line[0]][0].send_data(port_map[line[0]][1], line[1][0:-1])
            print("Completed")
        except IOError:
            print("! FILE ERROR !")


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

    # абстрактный метод
    def do(self):
        raise NotImplementedError('! USE OF BASE CLASS METHOD !')

    # добавляет (справа) значение в очередь <portname> и выполняет метод do() текущего узла
    def send_data(self, portname, value):
        if portname in self.ports.keys():
            if self.ports[portname] is not None:
                self.ports[portname].append(value)
            else:
                print("! NO PORT WITH NAME: ", portname, " !")
        has_empty = False
        for i in self.ports:
            if self.ports[i] != portname and len(self.ports[i]) == 0:
                has_empty = True
        if not has_empty:
            self.do()

    # снимает последнее (правое) значение с очереди <portname>
    def get_data(self, portname):
        if portname in self.ports.keys():
            return self.ports[portname].pop()

    # указывает следующий узел <other> графа и его очередь <portname>
    def link(self, other, portname):
        self.other = other
        self.otherPort = portname

    def __add__(self, other_node):
        # TODO: sum_node.link(mul_node, 'multiplier1') -> sum_node += mul_node
        # self.link(other_node, )
        pass

    # помещает значение <value> в очередь следующего узла (other)
    def send_result(self, value):
        if self.other is not None:
            self.other.send_data(self.otherPort, value)

    # переопределение оператора []
    def __getitem__(self, key):
        return self.ports[key]

    def __getattr__(self, key):
        # TODO: добавить проверку, что key не совпадает с output например
        if key not in self.ports:  # ????????????????????????????????????????????
            return self[key]


class Sum(Operation):  # обрабатывает событие суммы
    def __init__(self):  # инициализирует объект суммы
        super(Sum, self).__init__()
        self.type = 'SUM'
        self._add_port('term1')
        self._add_port('term2')
        self._add_port('result')
        self.term1 = 0
        self.term2 = 0

    def do(self):  # метод суммы
        self['result'] = int(self.get_data('term1')) + int(self.get_data('term2'))
        self.send_result(self['result'])


class Mul(Operation):  # обрабатывает событие умножения
    def __init__(self):  # инициализирует объект умножения
        super(Mul, self).__init__()
        self.type = 'MUL'
        self._add_port('multiplier1')
        self._add_port('multiplier2')
        self._add_port('result')
        self.multiplier1 = 0
        self.multiplier2 = 0

    def do(self):  # метод умножения
        self['result'] = int(self.get_data('multiplier1')) * int(self.get_data('multiplier2'))
        self.send_result(self['result'])


class Concat(Operation):  # обрабатывает событие конкатенации
    def __init__(self):  # инициализирует объект конкатенации
        super(Concat, self).__init__()
        self.type = 'CONCAT'
        self._add_port('string1')
        self._add_port('string2')
        self._add_port('result')
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
    # описание узлов
    sum_node = Sum()
    mul_node = Mul()
    concat_node = Concat()
    result_node = Result()
    port_map = {'A': (sum_node, 'term1'),
                'B': (sum_node, 'term2'),
                'M': (mul_node, 'multiplier2'),
                'C': (concat_node, 'string2')}

    print("sum_node initialized with operands: ", sum_node.get_ports())
    print("mul_node initialized with operands: ", mul_node.get_ports())
    print("concat_node initialized with operands: ", concat_node.get_ports())
    print("result_node initialized with operands: ", result_node.get_ports())

    # соединение узлов в граф
    sum_node.link(mul_node, 'multiplier1')
    #
    mul_node.link(concat_node, 'string1')
    concat_node.link(result_node, 'conclusion')
    # чтение данных из файла в порты узлов и выполнение do()
    file_reading()

    print("sum_node's operands after file_reading: ", sum_node.get_ports())
    print("mul_node's operands after file_reading: ", mul_node.get_ports())
    print("concat_node's operands after file_reading: ", concat_node.get_ports())
    print("result_node's operands after file_reading: ", result_node.get_ports())

    print()
    result_node.do()
