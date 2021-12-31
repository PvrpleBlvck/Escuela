import unittest

import main

class TestSM35(unittest.TestCase):
	def test_sum_multiples(self):
		self.assertEqual(main.app(1,10),23)
		self.assertEqual(main.app(1,100),2318)
		self.assertEqual(main.app(1,1000),233168)
		self.assertEqual(main.app(1,10123), 23915250)


if __name__ == '__main__':
	unittest.main(argv=['first-arg-is-ignored'], exit=False)