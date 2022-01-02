import unittest

import main

class TestPvrple(unittest.TestCase):
	def test_palindrome(self):
		self.assertTrue(main.pvrple(),906609)


if __name__ == '__main__':
	unittest.main(argv=['first-arg-is-ignored'], exit=False)