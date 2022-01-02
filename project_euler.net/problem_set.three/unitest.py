import unittest

import main

class BestPrimeTest(unittest.TestCase):
	def test_biggest_prime(self):
		self.assertEqual(main.Biggest_Prime_Factor(600851475143),6857) # Return true
		self.assertEqual(main.Biggest_Prime_Factor(6008514),58907) # Return true
		self.assertEqual(main.Biggest_Prime_Factor(5143),139) # Return true
		self.assertEqual(main.Biggest_Prime_Factor(6008),751) # Returned False 



if __name__ == '__main__':
	unittest.main(argv=['first-arg-is-ignored'], exit=False)		