import unittest
import calc

class TestCalc(unittest.TestCase):
	def test_addition(self):
		self.assertEqual(calc.addition(5, 5), 10)
		self.assertEqual(calc.addition(-3, 3), 0)
		self.assertEqual(calc.addition(-5, -5), -10)
	def test_subtraction(self):
		self.assertEqual(calc.subtraction(15, 5), 10)
		self.assertEqual(calc.subtraction(-1, 2), -3)
		self.assertEqual(calc.subtraction(-1, -1), 0)
	def test_multiplication(self):
		self.assertEqual(calc.multiplication(20, 5), 100)
		self.assertEqual(calc.multiplication(-2, 1), -2)
		self.assertEqual(calc.multiplication(-1, -3), 3)
	def test_division(self):
		self.assertEqual(calc.division(10, 10), 1)
		self.assertEqual(calc.division(-1, 1), -1)
		self.assertEqual(calc.division(-2, -2), 1)
		self.assertEqual(calc.division(6, 3), 2)
if __name__ == '__main__':
	unittest.main(argv=['first-arg-is-ignored'], exit=False)