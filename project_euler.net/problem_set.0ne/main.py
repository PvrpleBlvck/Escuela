#define a range of numbers to loop through
#multiples = int(input('Please enter a number to loop through: '))

#define a variable to append the sum of numbers in the range


#Iterate through the list and check if a number is a multiple of 5 and 3
def app(init, num):
    sum = 0
#[m for m in range(multiples) if not m % 5 or not m % 3]
    for m in range(init, num):
        if not m % 5 or not m % 3:
            sum = sum + m
    print(sum)



app(1,10)
app(1,100)
app(1,1000)
app(1,10123)