
#first we define our fibonacci function
def fib():
    # x, y variable with respective values
        x,y = 0,1
        # here we use a while loop initialize it to true, so that it runs as long as our condition is not met. i.e 4billion
        while True:
            #Because our data is quite extensive, we use Yield instead of return
            yield x
            # x y and y will be equal to x+y, 
            x,y = y, x+y


    #Now our second function will be to only iterate/ yield/(return those fibonacci numbers that are even)
    def even(seq):
        #our function takes sequence as input and we use for loop to go through the list
        for number in seq:
            # A simple logic that checks if the numbers in the sequence are divisible by 2 the return the number
            if not number % 2:
                yield number
    # Our last function answers our question. Takes sequence as input.
    #Note: Our sequence only contains numbers that are even!!!!!!
    def under_four_billion(seq):
        #Again we use for loop and if function to check if the conditions are met.
        for number in seq:
            if number > 4000000:
                #if condition is met,we break and return our number.
                break
            yield number   

    #Finally we call our even fucntion which takes under_four_billion as input which then takes fib function as an argument
    print sum(even(under_four_billion(fib())))
