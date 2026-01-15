"""
Simple function example for basic assessment testing.

This demonstrates a straightforward recursive implementation
of the Fibonacci sequence. Good for testing TECHNICAL path.
"""


def fibonacci(n):
    """Calculate the nth Fibonacci number using recursion."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# Example usage
if __name__ == "__main__":
    for i in range(10):
        print(f"fib({i}) = {fibonacci(i)}")
