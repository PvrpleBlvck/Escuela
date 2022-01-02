def digitsSum(N):
    sum = 0
    for digit in str(N): 
      sum += int(digit)      
    return sum
