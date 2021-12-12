#### Ok, here is our problem


# Largest palindrome product.
> A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
> Find the largest palindrome made from the product of two 3-digit numbers.


### Ofcourse there better ways of doing this,a more radical way would be ti just use a for loop
pvrple=0
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
                    pass
