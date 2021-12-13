#
def Biggest_Prime_Factor(n):
    return next(n // i for i in range(1, n) if n % i == 0 and is_prime(n // i))
  
def is_prime(m):
    return all(m % i for i in range(2, m - 1))
  
print(Biggest_Prime_Factor(600851475143))
