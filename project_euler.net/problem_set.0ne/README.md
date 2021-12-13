#### Ok, here is our problem
> If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

> Find the sum of all the multiples of 3 or 5 below 1000.

# So how do we tackle problem
> This one is very easy::::::and so is running this. Please visit the readme file (https://github.com/PvrpleBlvck/Pvrple_Blvck_Learning)
- ## Step One

> This one is kind of self explanatory. No need to define our input as i did. 
>> multiples = int(input('Please enter a number to loop through: '))

> The most important step in this case is to initialize our sum variable
>> sum = 0

> Now we use for loop to go through our range starting from 1.
	for m in range(1,multiples):
	#Now we check to see if numbers in our list are multiples of  and 3.
     	if not m % 5 or not m % 3:
     	# If yes, now we add them to our sum variable ne after another. or example..the 3 + 5 + ....
         	sum = sum + m


# Thank you!!!!!!!!!!!!!!!!!!