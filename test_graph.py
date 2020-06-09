# -*- coding: utf8 -*-

from yapipe import *
import random
import time
import tracemalloc
import csv
from math import ceil


# разделение списка some_list на части длины parts_len
def parting(some_list, parts):
    part_len = ceil(len(some_list) / parts)
    return [some_list[part_len * k:part_len * (k+1)] for k in range(parts)]


# запись в csv файл
def csv_writer(data: list, path="output.csv"):
    with open(path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        for i in range(0, len(data)):
            writer.writerow(data[i])


def test_graph():
    print("Starting test_graph...")
    test_array = []  # список с узлами тестового графа
    linked_to_result = 0
    big_n = 32
    layers = 8
    random.seed(2031)

    # заполнение списка узлами случайного типа и нумерация этих узлов
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

    # разбиение узлов по ярусам
    parted_test_array = parting(test_array, layers)
    count_layer = 1
    for i in parted_test_array:
        for j in i:
            j.layer = count_layer
        count_layer += 1

    # построение дуг без нарушения ярусов
    for i in range(0, len(parted_test_array) - 1):
        count = 0
        for j in parted_test_array[i]:
            for r in parted_test_array[i + 1]:
                    # соединяем дугой найденный узел и текущий
                    if r.type == 'SUM':
                        if count % 2 == 0:
                            j.link(r, 'term1')
                        else:
                            j.link(r, 'term2')
                    elif r.type == 'MUL':
                        if count % 2 == 0:
                            j.link(r, 'multiplier1')
                        else:
                            j.link(r, 'multiplier2')
                    else:
                        if count % 2 == 0:
                            j.link(r, 'amount_of_terms')
                        else:
                            j.link(r, 'accuracy')
            count += 1

    # добавление узла Result для вывода результата (он всегда будет последним в списке)
    parted_test_array.append([Result()])
    parted_test_array[len(parted_test_array) - 1][0].number = len(test_array)
    parted_test_array[len(parted_test_array) - 1][0].layer = layers + 1

    # все узлы с пустыми other соединяем дугой с узлом Result
    for i in parted_test_array[len(parted_test_array) - 2]:
        i.link(parted_test_array[len(parted_test_array) - 1][0], 'conclusion')
        linked_to_result += 1
    print(linked_to_result, " nodes are linked to RESULT node")

    test_array = []
    for i in parted_test_array:
        for j in i:
            test_array.append(j)

    get_visualization(test_array)

    # начало отсчета времени и памяти для рекурсивных режимов
    if (settings["mode"] == 0 or settings["mode"] == 2) and settings["monitoring"] == 1:
        start_time = time.time()
        tracemalloc.start()

    # всем узлам, в которые не входят дуги, заполняем порты
    if settings["mode"] == 2:
        with ThreadPoolExecutor(max_workers=4) as executor:
            def send_async(i, name, value):
                return executor.submit(test_array[i].send_data, name, value)

            pending_tasks = []
            for i in range(0, len(test_array)):
                if test_array[i].amount_of_previous == 0:
                    if test_array[i].type == 'SUM':
                        pending_tasks.append(send_async(i, 'term1', 2))
                        pending_tasks.append(send_async(i, 'term2', 2))
                    elif test_array[i].type == 'MUL':
                        pending_tasks.append(send_async(i, 'multiplier1', 2))
                        pending_tasks.append(send_async(i, 'multiplier2', 2))
                    else:
                        pending_tasks.append(send_async(i, 'amount_of_terms', 2))
                        pending_tasks.append(send_async(i, 'accuracy', 1.01))
            for t in pending_tasks:
                r = t.result()
    else:
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

    if settings["mode"] == 1:
        print("Executing the graph, mode 1...")
        if settings["monitoring"] == 1:
            start_time = time.time()
            tracemalloc.start()
        for i in range(0, len(test_array)):
            for j in range(0, 2**(layers+1)):
                try_do(test_array[i])

    if settings["mode"] == 3:
        print("Processing the graph, mode 3...")
        if settings["monitoring"] == 1:
            start_time = time.time()
            tracemalloc.start()
        for j in range(0, 2 ** (layers + 1)):
            process_tier_parallel_form(test_array)

    print("Test_graph completed!")

    if settings["monitoring"] == 1:
        t = str(round(time.time() - start_time, 2))
        if len(t) < 4:  # для правильной записи в CSV файл
            t += '0'
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("--- %s seconds ---" % t)
        print(f"--- Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 4}MB ---")
        monitoring_list = [[settings["mode"], t.replace('.', ','), str(peak / 10 ** 4).replace('.', ',')]]
        csv_writer(monitoring_list)
    print()


if __name__ == "__main__":
    for d in range(0, 40):
        if d >= 10:
            settings["mode"] = 2
        if d >= 20:
            settings["mode"] = 1
        if d >= 30:
            settings["mode"] = 0
        print("test_graph starts with mode = ", settings["mode"])
        test_graph()
