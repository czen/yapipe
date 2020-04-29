# -*- coding: utf8 -*-

from collections import deque


# чтение из файла
def file_reading():
    with open("in.txt") as f:
        if f:
            print("Reading file...")
            for line in f:
                line = line.split('=')
                if line[0] in port_map:
                    if len(port_map[line[0]][0].other) != 0:
                        port_map[line[0]][0].send_data(port_map[line[0]][1], line[1][0:-1])
        else:
            print("ERROR [in file_reading]: file error !")


class Operation(object):  # базовый класс
    def __init__(self):
        self.ports = dict()  # Словарь со всеми портами узла
        self.other = []  # Список следующих узлов
        self.otherPort = []  # список портов следующих узлов, куда передается результат
        self.color = 'white'  # "цвет" вершины (для поиска в глубину)
        self.number = -1  # Номер вершины

    # топологическая сортировка вершин
    # Вызывается от первого узла, параметр i не указывать при вызове
    # TODO: 5) Алгоритм Тарьяна - после покраски в черный цвет заносить вершину в глобальный список; обратный порядок
    #  следования этих вершин и будет правильной нумерацией
    def sort_nodes(self):
        if self.color == 'black':
            pass
        elif self.color == 'gray':
            print("ERROR [in sort_nodes]: loop found, topological sorting is impossible")
        elif self.color == 'white':
            self.color = 'gray'
            if len(self.other) != 0 and self.type != 'RESULT':
                for i in range(0, len(self.other)):
                    self.other[i].sort_nodes()
                self.color = 'black'
            elif self.type == 'RESULT':
                self.color = 'black'
            elif self.other is None:
                print("ERROR[in sort_nodes]: missing pointer to next node")

    # создает очередь <portname>
    def _add_port(self, portname):
        self.ports[portname] = deque()

    # возвращает список портов
    def get_all_ports(self):
        return self.ports

    # абстрактный метод
    def do(self):
        raise NotImplementedError("ERROR: the call of an abstract method do()")

    # добавляет (справа) значение в очередь <portname> и выполняет метод do() текущего узла
    def send_data(self, portname, value):
        if portname in self.ports.keys():
            self.ports[portname].append(value)
        else:
            print('ERROR [in send_data]: no port with name: ', portname)
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
        else:
            print("ERROR [in get_data]: argument is not a name of port")

    # указывает следующий узел <other> графа и его очередь <portname>
    def link(self, other, portname):
        self.other.append(other)
        self.otherPort.append(portname)

    # помещает значение <value> в очередь следующего узла (other)
    def send_result(self, value):
        if len(self.other) != 0:
            for i in range(0, len(self.other)):
                self.other[i].send_data(self.otherPort[i], value)
        else:
            print("ERROR [in send_result]: other is empty (no next node)")

    # возвращает пару (<узел>, <имя порта>) //кортеж
    def get_port(self, key):
        return self, key

    # <объект класса>.<имя порта>  ->  (узел, имя порта)
    def __getattr__(self, key):
        if key in self.ports:
            return self.get_port(key)
        else:
            return "ERROR [in __getattr__]: argument is not a name of port"

    # <объект класса>(<объект класса>.<имя порта>)  ->  <объект класса>.link(<объект класса>, <имя порта>)
    def __call__(self, other):
        if isinstance(other[0], Operation):
            self.link(other[0], other[1])
        else:
            return "ERROR [in __call__]: argument is not a subclass of Operation"


class Sum(Operation):  # обрабатывает событие суммы
    def __init__(self):  # инициализирует объект суммы
        super(Sum, self).__init__()
        self.type = 'SUM'
        self._add_port('term1')
        self._add_port('term2')

    def do(self):  # метод суммы
        val = int(self.get_data('term1')) + int(self.get_data('term2'))
        self.send_result(val)


class Mul(Operation):  # обрабатывает событие умножения
    def __init__(self):  # инициализирует объект умножения
        super(Mul, self).__init__()
        self.type = 'MUL'
        self._add_port('multiplier1')
        self._add_port('multiplier2')

    def do(self):  # метод умножения
        val = int(self.get_data('multiplier1')) * int(self.get_data('multiplier2'))
        self.send_result(val)


class Concat(Operation):  # обрабатывает событие конкатенации
    def __init__(self):  # инициализирует объект конкатенации
        super(Concat, self).__init__()
        self.type = 'CONCAT'
        self._add_port('string1')
        self._add_port('string2')

    def do(self):  # метод конкатенации
        val = str(self.get_data('string1')) + self.get_data('string2')
        self.send_result(val)


class Result(Operation):  # обрабатывает событие завершения процесса
    def __init__(self):  # инициализирует завершающий объект
        super(Result, self).__init__()
        self.type = 'RESULT'
        self._add_port('conclusion')

    def do(self):  # метод вывода результата
        if len(self.ports['conclusion']) != 0:
            print("CONCLUSION = ", self.ports['conclusion'])
        else:
            print("CONCLUSION is empty")


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
    # соединение узлов в граф
    sum_node(mul_node.multiplier1)
    mul_node(concat_node.string1)
    concat_node(result_node.conclusion)
    # чтение данных из файла в порты узлов и выполнение do()
    file_reading()
    print("Must be: 30 yapipe is done!")
    # топологическая сортировка
    sum_node.sort_nodes()
    print("sum_node color: ", sum_node.color, sum_node.number)
    print("mul_node color: ", mul_node.color, mul_node.number)
    print("concat_node color: ", concat_node.color, concat_node.number)
    print("result_node color: ", result_node.color, result_node.number)
