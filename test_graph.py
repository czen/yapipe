# -*- coding: utf8 -*-

from yapipe import *
import random
import time
import os
import psutil
import csv


# запись в csv файл (параметр data должен быть iterable)
def csv_writer(data, path="output.csv"):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range(0, len(data)):
            data[i] = str(data[i]).split(',')
            writer.writerow(data[i])


# для работы фукции sorted по полю .number
def byNumber_key(node):
    return node.number


def test_graph():
    print("Starting test_graph...")
    test_array = []  # список с узлами тестового графа
    if settings["monitoring"] == 1:
        monitoring_list = []
    # заполнение списка узлами случайного типа и нумерация этих узлов
    big_n = random.randint(1000, 5000)
    for i in range(0, big_n):
        z = random.randint(0, 4)
        if z == 0:
            test_array.append(Sum())
        elif z == 1:
            test_array.append(Mul())
        elif z == 2:
            test_array.append(CountAperi())
        elif z == 3:
            test_array.append(CountPi())
        else:
            test_array.append(CountE())
        test_array[i].number = i
    print("test_array created with amount of nodes: ", len(test_array))
    # print(test_array)
    random.shuffle(test_array)  # перемешивание списка
    # print("test_array shuffled: ")
    # print(test_array)
    # построение дуг без нарушения нумерации
    for i in range(0, len(test_array)):  # для каждого узла
        count = 0  # счетчик
        for k in range(0, len(test_array)):  # проходим по всему списку узлов
            # находим 2 узла с номерами < текущего
            if count < 2:
                if test_array[k].number < test_array[i].number:
                    if random.randint(0, big_n//10) == 1:  # соединяем, если выпадает 1
                        # соединяем дугой найденный узел и текущий
                        if test_array[i].type == 'SUM':
                            if count == 0:
                                test_array[k].link(test_array[i], 'term1')
                                count += 1
                            else:
                                test_array[k].link(test_array[i], 'term2')
                                count += 1
                            # print("Node number ", test_array[k].number, "linked with node number ",
                            # test_array[i].number)
                        elif test_array[i].type == 'MUL':
                            if count == 0:
                                test_array[k].link(test_array[i], 'multiplier1')
                                count += 1
                            else:
                                test_array[k].link(test_array[i], 'multiplier2')
                                count += 1
                        else:
                            if count == 0:
                                test_array[k].link(test_array[i], 'amount_of_terms')
                                count += 1
                            else:
                                test_array[k].link(test_array[i], 'accuracy')
                                count += 1
                            # print("Node number ", test_array[k].number, "linked with node number ",
                            # test_array[i].number)
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
    get_visualization(test_array)
    # начало отсчета времени и памяти для рекурсивного режима
    if settings["mode"] == 0 and settings["monitoring"] == 1:
        start_time = time.time()
        process = psutil.Process(os.getpid())
    # всем узлам, в которые входят 0 или 1 дуга, соответственно заполняем порты
    for i in range(0, len(test_array)):
        if test_array[i].amount_of_previous == 0:
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term1', 2)
                test_array[i].send_data('term2', 2)
            elif test_array[i].type == 'MUL':
                test_array[i].send_data('multiplier1', 2)
                test_array[i].send_data('multiplier2', 2)
            else:
                test_array[i].send_data('amount_of_terms', 2)
                test_array[i].send_data('accuracy', 1.01)
        elif test_array[i].amount_of_previous == 1:
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term2', 1)
            elif test_array[i].type == 'MUL':
                test_array[i].send_data('multiplier2', 3)
            else:
                test_array[i].send_data('accuracy', 1.01)
        # замер памяти
        if settings["mode"] == 0 and settings["monitoring"] == 1:
            mem = process.memory_info().rss / 1024 / 1024
            monitoring_list.append(round(mem, 2))
    if settings["mode"] == 1:
        test_array = sorted(test_array, key=byNumber_key)
        # print("test_array sorted:")
        # print(test_array)
        print("Executing the graph...")
        # начало отсчета времени для режима в порядке правильной нумерации
        if settings["monitoring"] == 1:
            start_time = time.time()
            process = psutil.Process(os.getpid())
        for i in range(0, len(test_array) - 1):  # выполнение всех узлов, кроме Result
            test_array[i].do()
            mem = process.memory_info().rss / 1024 / 1024
            monitoring_list.append(round(mem, 2))
            if i % (round(len(test_array) / 10)) == 0:  # при выполнении замеров отключать вывод *
                print(" * ", end="")
        print()
        test_array[len(test_array) - 1].do()  # выполнение узла Result
    print("RESULT do ", test_array[len(test_array) - 1].count, " of ", linked_to_result, "linked to it")
    print("Test_graph completed!")
    if settings["monitoring"] == 1:
        t = round(time.time() - start_time, 2)
        print("--- %s seconds ---" % t)
        monitoring_list.append(t)
        csv_writer(monitoring_list)


if __name__ == "__main__":
    print("test_graph starts with mode = ", settings["mode"])
    test_graph()
