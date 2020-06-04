# -*- coding: utf8 -*-

from decimal import *
from collections import deque
from graphviz import Digraph
from config import settings
from concurrent.futures import ThreadPoolExecutor

gl = []  # для проверки результатов выполнения тестовых запусков


class Operation(object):  # базовый класс
    def __init__(self):
        self.type = 'OPERATION'  # строка с названием операции
        self.ports = dict()  # Словарь со всеми портами узла
        self.other = []  # Список следующих узлов
        self.otherPort = []  # список портов следующих узлов, куда передается результат
        self.color = 'white'  # "цвет" вершины (для поиска в глубину)
        self.number = -1  # Номер вершины
        self.amount_of_previous = 0  # количество предыдущих узлов
        self.layer = -1

    # топологическая сортировка вершин (вызывается от первого узла), заполняет список узлами
    # в порядке правильной нумерации графа
    def sort_nodes(self, nodes: list):
        if self.color == 'black':
            pass
        elif self.color == 'gray':
            print("ERROR [in sort_nodes, node number ", self.number, "]: loop found, topological sorting is impossible")
        elif self.color == 'white':
            self.color = 'gray'
            if len(self.other) != 0 and self.type != 'RESULT':
                for i in range(0, len(self.other)):
                    self.other[i].sort_nodes(nodes)
                self.color = 'black'
                nodes.append(self)
            elif self.type == 'RESULT':
                self.color = 'black'
                nodes.append(self)
            elif self.other is None:
                print("WARNING [in sort_nodes , node number ", self.number, "]: missing pointer to next node")

    # создает очередь <portname>
    def _add_port(self, portname):
        self.ports[portname] = deque()

    # возвращает список портов
    def get_all_ports(self):
        return self.ports

    # абстрактный метод
    def do(self):
        print("WARNING [in do, node number ", self.number, "]: the call of an abstract method do()")

    # добавляет (справа) значение в очередь <portname> и выполняет метод do() текущего узла
    def send_data(self, portname, value):
        if portname in self.ports.keys():
            self.ports[portname].append(value)
        else:
            print("ERROR [in send_data, node number ", self.number, "]: no port with the name: ", portname)
        if settings["mode"] == 0 or settings["mode"] == 2:
            # попытка выполнить do для рекурсивного режима работы
            has_empty = False
            for i in self.ports:
                if self.ports[i] != portname and len(self.ports[i]) == 0:
                    has_empty = True
            if not has_empty:
                self.do()

    # снимает последнее (правое) значение с очереди <portname>
    def get_data(self, portname):
        if portname in self.ports.keys():
            if len(self.ports[portname]) != 0:
                return self.ports[portname].pop()
            else:
                print("ERROR [in get_data, node number ", self.number, "]: port ", portname, " is empty")
        else:
            print("ERROR [in get_data, node number ", self.number, "]: argument is not a name of port")

    # указывает следующий узел <other> графа и его очередь <portname>
    def link(self, other, portname):
        self.other.append(other)
        self.otherPort.append(portname)
        other.amount_of_previous += 1

    # помещает значение <value> в очередь следующего узла (other)
    def send_result(self, value):
        if len(self.other) != 0:
            for i in range(0, len(self.other)):
                self.other[i].send_data(self.otherPort[i], value)
        else:
            print("ERROR [in send_result, node number ", self.number, "]: other is empty (no next node)")

    # возвращает пару (<узел>, <имя порта>) //кортеж
    def get_port(self, key):
        return self, key

    # <объект класса>.<имя порта>  ->  (узел, имя порта)
    def __getattr__(self, key):
        if key in self.ports:
            return self.get_port(key)
        else:
            return "ERROR [in __getattr__ ", self.number, "]: argument is not a name of port"

    # <объект класса>(<объект класса>.<имя порта>)  ->  <объект класса>.link(<объект класса>, <имя порта>)
    def __call__(self, other):
        if isinstance(other[0], Operation):
            self.link(other[0], other[1])
        else:
            return "ERROR [in __call__ ", self.number, "]: argument is not a subclass of Operation"


# классы - наследники
class Sum(Operation):  # сумма
    def __init__(self):
        super(Sum, self).__init__()
        self.type = 'SUM'
        self._add_port('term1')
        self._add_port('term2')

    def do(self):  # метод суммы
        val = Decimal(self.get_data('term1')) + Decimal(self.get_data('term2'))
        # print("SUM node number ", self.number, " done with val = ", val)
        # for i in range(0, len(self.other)-1):
        #    print("     and val is sent to node number ", self.other[i].number)
        self.send_result(val)


class Mul(Operation):  # умножение
    def __init__(self):
        super(Mul, self).__init__()
        self.type = 'MUL'
        self._add_port('multiplier1')
        self._add_port('multiplier2')

    def do(self):  # метод умножения
        val = Decimal(self.get_data('multiplier1')) * Decimal(self.get_data('multiplier2'))
        # print("MUL node number ", self.number, " done with val = ", val)
        # for i in range(0, len(self.other) - 1):
        #     print("     and val is sent to node number ", self.other[i].number)
        self.send_result(val)


class Concat(Operation):  # конкатенация
    def __init__(self):
        super(Concat, self).__init__()
        self.type = 'CONCAT'
        self._add_port('string1')
        self._add_port('string2')

    def do(self):  # метод конкатенации
        val = str(self.get_data('string1')) + str(self.get_data('string2'))
        # print("CONCAT node number ", self.number, " done with val = ", val)
        # for i in range(0, len(self.other) - 1):
        #     print("     and val is sent to node number ", self.other[i].number)
        self.send_result(val)


class CountAperi(Operation):  # вычисление числа ζ(3) (Постоянная Апери)
    def __init__(self):
        super(CountAperi, self).__init__()
        self.type = 'COUNT_APERI'
        self._add_port('amount_of_terms')  # количеством суммируемых членов ряда будет значение этого поля * 1000
        self._add_port('accuracy')  # точностью будет количество значащих знаков после запятой в этом поле

    def do(self):  # метод подсчета суммы обратных кубов
        # выделяем значащие знаки после запятой значения поля accuracy
        z = Decimal(str(self.get_data('accuracy')))
        z = z - int(z)
        val = Decimal(0)
        n = round(self.get_data('amount_of_terms')) * 1000
        for i in range(1, n):
            val += Decimal('1') / (Decimal(i ** 3))
        self.send_result(val.quantize(Decimal(z)))


class CountPi(Operation):  # вычисление числа π (пи)
    def __init__(self):
        super(CountPi, self).__init__()
        self.type = 'COUNT_PI'
        self._add_port('amount_of_terms')  # количеством суммируемых членов ряда будет значение этого поля * 1000
        self._add_port('accuracy')  # точностью будет количество значащих знаков после запятой в этом поле

    def do(self):  # метод подсчета суммы Ряда Лейбница, умноженной на 4
        # выделяем значащие знаки после запятой значения поля accuracy
        z = Decimal(str(self.get_data('accuracy')))
        z = z - int(z)
        val = Decimal(0)
        n = round(self.get_data('amount_of_terms')) * 1000
        for i in range(0, n):
            val += Decimal((-1) ** i) / Decimal(2 * i + 1)
        val = val * 4
        self.send_result(val.quantize(Decimal(z)))


class CountE(Operation):  # вычисление числа e (число Эйлера)
    def __init__(self):
        super(CountE, self).__init__()
        self.type = 'COUNT_E'
        self._add_port('amount_of_terms')  # количеством суммируемых членов ряда будет значение этого поля * 10
        self._add_port('accuracy')  # точностью будет количество значащих знаков после запятой в этом поле

    def do(self):  # метод вычисления суммы ряда (1/n!), n = 0..inf
        # выделяем значащие знаки после запятой значения поля accuracy
        z = Decimal(str(self.get_data('accuracy')))
        z = z - int(z)
        val = Decimal(0)
        n = round(self.get_data('amount_of_terms')) * 10
        for i in range(0, n):
            fac = 1
            for j in range(2, i + 1):
                fac *= j
            val += Decimal('1') / Decimal(fac)
        self.send_result(val.quantize(Decimal(z)))


class Result(Operation):  # завершение процесса
    def __init__(self):
        super(Result, self).__init__()
        self.type = 'RESULT'
        self._add_port('conclusion')
        self.count = 0  # поле - счетчик для посчета количества выполнений do

    def do(self):  # метод вывода результата
        if len(self.ports['conclusion']) != 0:
            if settings["mode"] == 0 or settings["mode"] == 2:
                self.count += 1
                res = self.ports['conclusion'].pop()
                gl.append(res)
                print("CONCLUSION ", self.count, "at node number ", self.number, " = ", res)
            elif settings["mode"] == 1 or settings["mode"] == 3:
                for i in range(0, len(self.ports['conclusion'])):
                    self.count += 1
                    res = self.ports['conclusion'].popleft()
                    gl.append(res)
                    print("CONCLUSION ", self.count, " at node number ", self.number, " = ", res)
        else:
            print("CONCLUSION at node number ", self.number, " is empty")


# визуализация графа в файл test-output/TestGraph
# для вызывается от списка узлов
def get_visualization(nodes: list):
    dot = Digraph(comment='Test graph')  # для визуализации с помощью graphviz
    if settings["rendering"] == 1:
        for i in range(0, len(nodes)):
            dot.node(str(nodes[i].number), nodes[i].type + ' ' + str(nodes[i].number))
        for i in range(0, len(nodes)):
            if len(nodes[i].other) > 0:
                for j in range(0, len(nodes[i].other)):
                    dot.edge(str(nodes[i].number), str(nodes[i].other[j].number))
        print("Rendering...")
        dot.render('test-output/TestGraph.gv', view=True)
    else:
        print("Rendering disabled in config.py")


# нумерует узлы в порядке следования в списке
def get_numeration(nodes: list):
    nodes.reverse()
    for i in range(0, len(nodes)):
        nodes[i].number = i


# вывод правильной нумерации графа
def print_numeration(nodes: list):
    print("Correct graph numeration:")
    for i in nodes:
        print("    ", i.type, " - ", i.number)


# попытка выполнить do для режима работы в порядке правильной нумерации
def try_do(node: Operation):
    has_empty = False
    for p in node.ports:
        if len(node.ports[p]) == 0:
            has_empty = True
    if not has_empty:
        node.do()


# рекурсивный обход узлов и присваивание номера яруса
def set_layer(node: Operation, layer):
    if node.layer < layer:
        node.layer = layer
        layer += 1
    if len(node.otherPort) > 0:
        for i in node.other:
            set_layer(i, layer)


# ярусно-параллельная форма графа
def get_tier_parallel_form(nodes: list, layer=2):
    for i in nodes:
        if i.amount_of_previous == 0:
            i.layer = 1
            for j in i.other:
                set_layer(j, layer)


# вывод ярусно-параллельной формы графа
def print_tier_parallel_form(nodes: list):
    print("Tire Parallel form:")
    for i in nodes:
        print("    ", i.type, " - ", i.layer)


def process_tier_parallel_form(nodes: list):
    max_layer = 0
    for i in nodes:
        if i.layer > max_layer:
            max_layer = i.layer
    with ThreadPoolExecutor(max_workers=4) as executor:
        def do_async(node):
            return executor.submit(node.do)

        pending_tasks = []
        for j in range(1, max_layer + 1):
            for i in nodes:
                if i.layer == j:
                    has_empty = False
                    for p in i.ports:
                        if len(i.ports[p]) == 0:
                            has_empty = True
                    if not has_empty:
                        pending_tasks.append(do_async(i))
        for task in pending_tasks:
            res = task.result()


# чтение данных из файла в порты узлов и выполнение графа
def file_reading(nodes: list, datamap: {}):
    with open("in.txt") as f:
        if f:
            print("Reading file...")
            for line in f:
                line = line.split('=')
                if line[0] in datamap:
                    if len(datamap[line[0]][0].other) != 0:
                        datamap[line[0]][0].send_data(datamap[line[0]][1], line[1][0:-1])
            print("File is read")
            if settings["mode"] == 1:
                for i in nodes:
                    try_do(i)
            elif settings["mode"] == 3:
                process_tier_parallel_form(nodes)
        else:
            print("ERROR [in file_reading]: file error !")


if __name__ == "__main__":
    print("Yapipe starts with mode = ", settings["mode"])
    tar = []  # список для алгоритма Тарьяна
    sum_node1 = Sum()
    sum_node2 = Sum()
    mul_node = Mul()
    concat_node1 = Concat()
    concat_node2 = Concat()
    result_node1 = Result()
    result_node2 = Result()
    port_map = {'A1': (sum_node1, 'term1'),
                'B1': (sum_node1, 'term2'),
                'M': (mul_node, 'multiplier2'),
                'C1': (concat_node1, 'string2'),
                'B2': (sum_node2, 'term2')}
    # соединение узлов в граф:
    """
           sum2 -> concat -> res2 => ['30 yapipe is done!']
          ↗      ↗
    sum1 -> mul -> concat1 -> res1 => ['2030']
    """
    sum_node1(mul_node.multiplier1)
    sum_node1(sum_node2.term1)
    mul_node(concat_node1.string1)
    mul_node(concat_node2.string2)
    sum_node2(concat_node2.string1)
    concat_node1(result_node1.conclusion)
    concat_node2(result_node2.conclusion)
    sum_node1.sort_nodes(tar)
    get_numeration(tar)
    print_numeration(tar)
    get_tier_parallel_form(tar)
    print_tier_parallel_form(tar)
    file_reading(tar, port_map)
    print()
    print("     Must be: CONCLUSION  1  at node number  6  =  30 yapipe is done!")
    print("              CONCLUSION  1  at node number  4  = 2030")
