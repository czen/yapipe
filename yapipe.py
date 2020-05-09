# -*- coding: utf8 -*-

from collections import deque
import random

mode = 0  # режим работы (0 - рекурсивный, 1 - в порядке правильной нумерации)
# словарь с соответствием режимов работы и значением переменной mode
all_modes = {0: 'recursive', 1: 'in the order of the correct numeration'}
tar = []  # список для алгоритма Тарьяна


def byNumber_key(node):
    return node.number


# TODO: добавить graphviz
def test_graph():
    print("Starting test_graph...")
    test_array = []  # список с узлами тестового графа
    # заполнение списка узлами случайного типа и нумерация этих узлов
    for i in range(0, random.randint(100, 300)):
        z = random.randint(0, 1)
        if z == 0:
            test_array.append(Sum())
        else:
            test_array.append(Mul())
        test_array[i].number = i
    print("test_array created with amount of nodes: ", len(test_array))
    # print(test_array)
    random.shuffle(test_array)  # перемешивание списка
    # print("test_array shuffled: ")
    # print(test_array)
    # построение дуг без нарушения нумерации
    for i in range(0, len(test_array)):  # для всех узлов
        count = 0  # счетчик
        for k in range(0, len(test_array)):  # проходим по всем узлам
            # находим 2 узла с номерами < текущего
            if count < 2:
                if test_array[k].number < test_array[i].number:
                    # соединяем дугой найденный узел и текущий
                    if test_array[i].type == 'SUM':
                        if count == 0:
                            test_array[k].link(test_array[i], 'term1')
                            count += 1
                        else:
                            test_array[k].link(test_array[i], 'term2')
                            count += 1
                        # print("Node number ", test_array[k].number, "linked with node number ", test_array[i].number)
                    else:
                        if count == 0:
                            test_array[k].link(test_array[i], 'multiplier1')
                            count += 1
                        else:
                            test_array[k].link(test_array[i], 'multiplier2')
                            count += 1
                        # print("Node number ", test_array[k].number, "linked with node number ", test_array[i].number)
            else:
                break  # выход из цикла, когда нашли 2 узла с номерами < текущего
    # print("arcs selected")
    # добавление узла Result для вывода результата (он всегда будет последним в списке)
    test_array.append(Result())
    test_array[len(test_array) - 1].number = len(test_array) - 1
    # print("result added:")
    # print(test_array)
    # все узлы с пустыми other соединяем дугой с узлом Result
    linked_to_result = 0  # счетчик для подсчета узлов, соединенных с узлом Result
    for i in range(0, len(test_array) - 1):  # -1 исключает узел Result
        if len(test_array[i].other) == 0:
            test_array[i].link(test_array[len(test_array) - 1], 'conclusion')
            linked_to_result += 1
            # print("Node number ", test_array[i].number, "is linked with RESULT node")
    print(linked_to_result, " nodes are linked to RESULT node")
    # заполняем оба порта узлу с номером 0 и второй порт узлу с номером 1
    for i in range(0, len(test_array) - 1):  # -1 исключает узел Result
        if test_array[i].number == 0:
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term1', 1)
                test_array[i].send_data('term2', 1)
            else:
                test_array[i].send_data('multiplier1', 3)
                test_array[i].send_data('multiplier2', 3)
        if test_array[i].number == 1:
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term2', 1)
            else:
                test_array[i].send_data('multiplier2', 3)
    if mode == 1:
        test_array = sorted(test_array, key=byNumber_key)
        # print("test_array sorted:")
        # print(test_array)
        for i in range(0, len(test_array)):
            test_array[i].do()
    print("RESULT do ", test_array[len(test_array)-1].count, " of ", linked_to_result, "linked to it")
    print("Test_graph completed!")


# правильная нумерация вершин графа (вызывается после топологической сортировки)
def get_numeration():
    tar.reverse()
    print()
    print("Correct graph numeration:")
    for i in range(0, len(tar)):
        tar[i].number = i
        print("    ", tar[i], " - ", tar[i].number)


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
                        if mode == 1:
                            # попытка выполнить do для режима работы в порядке правильной нумерации
                            for i in range(0, len(tar)):
                                has_empty = False
                                for j in tar[i].ports:
                                    if len(tar[i].ports[j]) == 0:
                                        has_empty = True
                                if not has_empty:
                                    tar[i].do()
        else:
            print("ERROR [in file_reading]: file error !")


class Operation(object):  # базовый класс
    def __init__(self):
        self.ports = dict()  # Словарь со всеми портами узла
        self.other = []  # Список следующих узлов
        self.otherPort = []  # список портов следующих узлов, куда передается результат
        self.color = 'white'  # "цвет" вершины (для поиска в глубину)
        self.number = -1  # Номер вершины
        self.amount_of_previous = 0  # количество предыдущих узлов

    # топологическая сортировка вершин (вызывается от первого узла)
    def sort_nodes(self):
        if self.color == 'black':
            pass
        elif self.color == 'gray':
            print("ERROR [in sort_nodes, node number ", self.number, "]: loop found, topological sorting is impossible")
        elif self.color == 'white':
            self.color = 'gray'
            if len(self.other) != 0 and self.type != 'RESULT':
                for i in range(0, len(self.other)):
                    self.other[i].sort_nodes()
                self.color = 'black'
                tar.append(self)
            elif self.type == 'RESULT':
                self.color = 'black'
                tar.append(self)
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
        if mode == 0:
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


class Sum(Operation):  # обрабатывает событие суммы
    def __init__(self):  # инициализирует объект суммы
        super(Sum, self).__init__()
        self.type = 'SUM'
        self._add_port('term1')
        self._add_port('term2')

    def do(self):  # метод суммы
        val = int(self.get_data('term1')) + int(self.get_data('term2'))
        # print("SUM node number ", self.number, " done with val = ", val)
        # for i in range(0, len(self.other)-1):
        #    print("     and val is sent to node number ", self.other[i].number)
        self.send_result(val)


class Mul(Operation):  # обрабатывает событие умножения
    def __init__(self):  # инициализирует объект умножения
        super(Mul, self).__init__()
        self.type = 'MUL'
        self._add_port('multiplier1')
        self._add_port('multiplier2')

    def do(self):  # метод умножения
        val = int(self.get_data('multiplier1')) * int(self.get_data('multiplier2'))
        # print("MUL node number ", self.number, " done with val = ", val)
        # for i in range(0, len(self.other) - 1):
        #     print("     and val is sent to node number ", self.other[i].number)
        self.send_result(val)


class Concat(Operation):  # обрабатывает событие конкатенации
    def __init__(self):  # инициализирует объект конкатенации
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


class Result(Operation):  # обрабатывает событие завершения процесса
    def __init__(self):  # инициализирует завершающий объект
        super(Result, self).__init__()
        self.type = 'RESULT'
        self._add_port('conclusion')
        self.count = 0  # поле - счетчик для посчета количества выполнений do

    def do(self):  # метод вывода результата
        if len(self.ports['conclusion']) != 0:
            if mode == 0:
                self.count += 1
                print("CONCLUSION ", self.count, "at node number ", self.number, " = ",
                      self.ports['conclusion'].pop())
            elif mode == 1:
                for i in range(0, len(self.ports['conclusion'])):
                    self.count += 1
                    print("CONCLUSION ", self.count, " at node number ", self.number, " = ",
                          self.ports['conclusion'].popleft())
        else:
            print("CONCLUSION at node number ", self.number, " is empty")


if __name__ == "__main__":
    # описание узлов
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
    # соединение узлов в граф
    #
    #        sum2 -> concat -> res2 => ['30 yapipe is done!']
    #       ↗      ↗
    # sum1 -> mul -> concat1 -> res1 => ['2030']
    #
    sum_node1(mul_node.multiplier1)
    sum_node1(sum_node2.term1)
    mul_node(concat_node1.string1)
    mul_node(concat_node2.string2)
    sum_node2(concat_node2.string1)
    concat_node1(result_node1.conclusion)
    concat_node2(result_node2.conclusion)
    # топологическая сортировка
    sum_node1.sort_nodes()
    get_numeration()
    # выбор режима работы
    print("Choose mode: ", all_modes)
    mode = int(input())
    if mode in all_modes.keys():
        # чтение данных из файла в порты узлов и выполнение do()
        file_reading()
        print("Must be: 30 yapipe is done!")
        print("         2030")
        print()
        print("Do u need to start test_graph? (Y - yes)")
        ch = input()
        if ch == "Y" or ch == "y":
            test_graph()
    else:
        print("ERROR [in choosing mode]: no such mode")
