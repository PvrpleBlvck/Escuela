#### Ok, here is our problem


# Largest palindrome product.
> A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
> Find the largest palindrome made from the product of two 3-digit numbers.


### Ofcourse there're better ways of doing this,a more radical way would be to just use a for loop

>
""" pvrple=0
>
for a in range(999,99,-1):
    for b in range(999,99,-1):
                c=a*b
                d=len(str(c))
                e=list(str(c)[0:d/2])
                f=list(str(c)[d/2:])
                f.reverse()
                if e==f:
                    if c>pvrple:
                        pvrple=c
                        print c,a,b
                    else:
                        pass    
                else :
                    pass """


### Now i am going to conduct unit testing for this code


> So first we import unittest which is a builtin module as
 ### import unittest
 > Secondly we import our python file as
 ### import main.py
 ## we define a class and name it anything, am naming mine as below and we pass unittest.TestCase as arg
> class clsName(unittest.TestCase):
# Now we define a function that's and pass in (self), remember if you don't pass (self), you will run into TypeError
>    def funcName(self):
### From there we just initialize our func . This time we use self.assertTrue
> self.assertTrue(main.pvrple(),arg)
> Everything looks perfect, now let's run our python file. 
### python unitest.py

----------------------------------------------------------------------
### Ran 1 test in 25.301s

### OK
> That's the results, which means everything is well set.

# Thank you If there's anything you would love add to please do not hesitate to make a contribution or get in touch with for any corrections, questions and or assistance!
