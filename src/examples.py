"""Example codes for the AI Python C Extensions Generator application."""

# Prints 'Hello, World!' from a Python function.
example_hello_world = """
def hello_world():
    print("Hello, World!")
"""

# Iterates over an array and returns the sum of all its elements.
example_sum = """
def array_sum(arr):
    total = 0
    for x in arr:
        total += x
    return total
"""

# Returns the nth Fibonacci number using an iterative approach.
example_fibonacci = """
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
"""

# Approximates π using the Leibniz alternating series formula.
example_leibniz_pi = """
def leibniz_pi(iterations):
    result = 1.0
    for i in range(1, iterations + 1):
        j = i * 4 - 1
        result -= (1 / j)
        j = i * 4 + 1
        result += (1 / j)
    return result * 4
"""

# Finds the total maximum subarray sum over 20 runs using LCG RNG.
example_subarray = """
def lcg(seed, a=1664525, c=1013904223, m=2**32):
    value = seed
    while True:
        value = (a * value + c) % m
        yield value

def max_subarray_sum(n, seed, min_val, max_val):
    lcg_gen = lcg(seed)
    random_numbers = [next(lcg_gen) % (max_val - min_val + 1) + min_val
                      for _ in range(n)]
    max_sum = float('-inf')
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += random_numbers[j]
            if current_sum > max_sum:
                max_sum = current_sum
    return max_sum

def total_max_subarray_sum(n, initial_seed, min_val, max_val):
    total_sum = 0
    lcg_gen = lcg(initial_seed)
    for _ in range(20):
        seed = next(lcg_gen)
        total_sum += max_subarray_sum(n, seed, min_val, max_val)
    return total_sum
"""

# Dictionary of examples for easy access in the interface.
example_dict = {
    "Hello world": [example_hello_world, "hello_world"],
    "Sum array": [example_sum, "array_sum"],
    "Fibonacci": [example_fibonacci, "fibonacci"],
    "Leibniz pi": [example_leibniz_pi, "calculate_pi"],
    "Max subarray sum": [example_subarray, "max_subarray_sum"]}
