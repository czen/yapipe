# -*- coding: utf8 -*-

from yapipe import *
import random


def byNumber_key(node):
    return node.number


def test_graph():
    print("Starting test_graph...")
    test_array = []  # список с узлами тестового графа
    # заполнение списка узлами случайного типа и нумерация этих узлов
    for i in range(0, random.randint(10, 20)):
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
    # визуализация графа
    get_visualization(test_array)
    # заполняем оба порта узлу с номером 0 и второй порт узлу с номером 1
    for i in range(0, len(test_array) - 1):  # -1 исключает узел Result
        if test_array[i].number == 0:  # для узла 0
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term1', 1)
                test_array[i].send_data('term2', 1)
            elif test_array[i].type == 'MUL':
                test_array[i].send_data('multiplier1', 3)
                test_array[i].send_data('multiplier2', 3)
            else:
                test_array[i].send_data('amount_of_terms', 3)
                test_array[i].send_data('accuracy', 1.0001)
        if test_array[i].number == 1:  # для узла 1
            if test_array[i].type == 'SUM':
                test_array[i].send_data('term2', 1)
            elif test_array[i].type == 'MUL':
                test_array[i].send_data('multiplier2', 3)
            else:
                test_array[i].send_data('accuracy', 1.0001)
    if settings["mode"] == 1:
        test_array = sorted(test_array, key=byNumber_key)
        # print("test_array sorted:")
        # print(test_array)
        print("Executing the graph...")
        for i in range(0, len(test_array) - 1):  # выполнение всех узлов, кроме Result
            test_array[i].do()
            if i % (round(len(test_array) / 10)) == 0:  # при выполнении замеров отключать вывод *
                print(" * ", end="")
        print()
        test_array[len(test_array) - 1].do()  # выполнение узла Result
    print("RESULT do ", test_array[len(test_array) - 1].count, " of ", linked_to_result, "linked to it")
    print("Test_graph completed!")


if __name__ == "__main__":
    print("test_graph starts with mode = ", settings["mode"])
    test_graph()
