"""
Simple function example for basic assessment testing.

This demonstrates a straightforward recursive implementation
of the Fibonacci sequence. Good for testing TECHNICAL path.
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n):
    """Calculate the nth Fibonacci number using recursion.

    Note: The plain recursive algorithm has exponential time
    complexity O(2^n). This version uses memoization via
    functools.lru_cache to provide much better performance
    while preserving the same recursive interface.
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Example usage
if __name__ == "__main__":
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
