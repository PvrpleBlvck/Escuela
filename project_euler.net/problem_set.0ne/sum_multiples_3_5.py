#define a range of numbers to loop through
multiples = int(input('Please enter a number to loop through: '))

#define a variable to append the sum of numbers in the range
sum = 0

#Iterate through the list and check if a number is a multiple of 5 and 3

#[m for m in range(multiples) if not m % 5 or not m % 3]
for m in range(1,multiples):
     if not m % 5 or not m % 3:
         sum = sum + m
print(sum)
