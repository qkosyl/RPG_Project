'''Example of Using Recursion

A good example of using recursion is the Fibonacci sequence. The Fibonacci sequence is a sequence where the first number is 0, the second number is 1, and the Nth number is the sum of the (N - 1) and (N - 2). So, the task is to write a function calculating the Nth element of a sequence.
You can solve this task with an ordinary loop:
def get_fib(n):
n_fib = None
if n < 1:
print('N must be > 0')
elif n == 1:
n_fib = 0
elif n == 2:
n_fib = 1
else:
prev_2, prev_1 = 0, 1
for i in range(2, n):
n_fib = prev_2 + prev_1
prev_2 = prev_1
prev_1 = n_fib
return n_fib

def get_fib(n):
        return get_fib(n-2) + get_fib(n-1)

Code
def get_fib(n):
    """Get a Nth element of the Fibonacci sequence."""
    if n == 1: # base case
        value = 0
    elif n == 2: # base case
        value = 1
    else:
        value = get_fib(n - 2) + get_fib(n - 1) # recursive call

    return value

Execution
get_fib(5)
3

get_fib(7)
8
'''