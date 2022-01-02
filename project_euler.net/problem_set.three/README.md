#### Ok, here is our problem

> The prime factors of 13195 are 5, 7, 13 and 29.
> What is the largest prime factor of the number 600851475143 ?

> Spoiler, the largest prime factor here is #6857

### Here we use Next function which returns the next item from an iterator.
> The next function takes two args
> next(iterator[, default])

> for example if we a list 
### x = [1,2,3,4,5]

> obj = iter(x)
> Now if call next(obj) ;for the first time it returns 1.
> Calling it again will return 2 and so so forth


### Now back to our first fucntion
>
	def Biggest_Prime_Factor(n):
    	return next(n // i for i in range(1, n) if n % i == 0 and is_prime(n // i))
> To put this in simple terms, the function returns an iteration of our func
> We loop through (n // (n) but only if n % returns 0 and [is_prime(n // 1)])
> Yes is_prime function ,comes next.
>
	def is_prime(m):
    	return all(m % i for i in range(2, m - 1))

> Here lets use a built in python function 'all', which returns true if all the elements of a given iterable( List, Dictionary, Tuple, set, etc) are True else it returns False. It also returns True if the iterable object is empty.

> I doubt this need an explanation, but if you need one. Hit me up!

> Lastly, we call our function and ta-da!

### Now i am going to conduct unit testing for this code


> So first we import unittest which is a builtin module as
 ### import unittest
 > Secondly we import our python file as
 ### import main.py
 ## we define a class and name it anything, am naming mine as below and we pass unittest.TestCase as arg
> class BestPrimeTest(unittest.TestCase):
# Now we define a function that's and pass in (self), remember if you don't pass (self), you will run into TypeError
>    def test_biggest_prime(self):
### From there we just initialize our func . 
> self.assertEqual(main.Biggest_Prime_Factor(600851475143),6857)
> Everything looks perfect, now let's run our python file. 
### python unitest.py

'''6857
58907
139
751
.'''
----------------------------------------------------------------------
### Ran 1 test in 25.301s

### OK
> That's the results, which means everything is well set.

# Thank you If there's anything you would love add to please do not hesitate to make a contribution or get in touch with for any corrections, questions and or assistance!
