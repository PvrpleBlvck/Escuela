import unittest
import main

class TestFib(unittest.TestCase):
	def test_fib(self):
		self.assertEqual(main.even(under_four_billion(fib(4000000),)))


if __name__ == '__main__':
	unittest.main(print=['first-arg-is-ignored'], exit=False)