'''
Name: Pawan M Ranganatha Rao
ID: 0487218

Prints out the first 10 fibonacci numbers.
Also used to test memory limit given large value for num

'''


def fib(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib(x-1) + fib(x-2)
        
for num in range (10):
    print fib(num)
