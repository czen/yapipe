# -*- coding: utf8 -*-

import unittest
from yapipe import *


class YapipeTest(unittest.TestCase):
    """yapipe tests"""

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        print("")

    def test_operation(self):
        """Operation test"""
        op = Operation()
        op._add_port('A')
        op.send_data('A', 1)
        val = op.get_data('A')
        self.assertEqual(1, val)

    def test_sum(self):
        """Sum test"""
        print("id: " + self.id())
        testobj = Sum()
        testobj2 = Sum()
        testobj2._add_port('R')
        testobj.link(testobj2, 'R')
        testobj.send_data('term1', 1)
        testobj.send_data('term2', 2)
        if settings["mode"] == 1:
            testobj.do()
        self.assertEqual(3, testobj2.get_data('R'))

    def test_mul(self):
        """Mul test"""
        print("id: " + self.id())
        testobj = Mul()
        testobj2 = Mul()
        testobj2._add_port('R')
        testobj.link(testobj2, 'R')
        testobj.send_data('multiplier1', 2)
        testobj.send_data('multiplier2', 3)
        if settings["mode"] == 1:
            testobj.do()
        self.assertEqual(6, testobj2.get_data('R'))

    def test_concat(self):
        """Concat test"""
        print("id: " + self.id())
        testobj = Concat()
        testobj2 = Concat()
        testobj2._add_port('R')
        testobj.link(testobj2, 'R')
        testobj.send_data('string1', "ya")
        testobj.send_data('string2', "pipe")
        if settings["mode"] == 1:
            testobj.do()
        self.assertEqual("yapipe", testobj2.get_data('R'))


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(exit=False)
