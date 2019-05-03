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
		op.addPort('A')
		op.sendData('A', 1)
		val = op.getData('A')
		self.assertEqual(1, val)

	def test_sum(self):
		"""Sum test"""
		print("id: " + self.id())
		testobj = Sum(1, 2)
		testobj.do()
		self.assertEqual(3, testobj.res)

	def test_mul(self):
		"""Mul test"""
		print("id: " + self.id())
		testobj = Mul(1, 3)
		testobj.do()
		self.assertEqual(3, testobj.res)

	def test_concat(self):
		"""Concat test"""
		print("id: " + self.id())
		testobj = Concat('ya', 'pipe')
		testobj.do()
		self.assertEqual('yapipe', testobj.res)

if __name__ == "__main__":
    # Запуск тестов
    unittest.main(exit=False)