"""
Code with tests example for comprehensive assessment.

This demonstrates testing awareness, separation of concerns,
and good documentation practices. Good for all assessment paths.
"""


def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: List of numeric values

    Returns:
        The arithmetic mean of the numbers

    Raises:
        ValueError: If the list is empty
        TypeError: If any element is not numeric
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")

    # Validate all elements are numeric
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError(f"Expected numeric value, got {type(num).__name__}")

    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median of a list of numbers.

    Args:
        numbers: List of numeric values

    Returns:
        The median value

    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate median of empty list")

    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)

    if length % 2 == 0:
        # Even number of elements: average of middle two
        mid1 = sorted_numbers[length // 2 - 1]
        mid2 = sorted_numbers[length // 2]
        return (mid1 + mid2) / 2
    else:
        # Odd number of elements: middle element
        return sorted_numbers[length // 2]


# Tests (demonstrates testing awareness)
def test_calculate_average():
    """Test average calculation with various inputs."""
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0
    assert calculate_average([10]) == 10.0
    assert calculate_average([2, 4]) == 3.0

    # Test error cases
    try:
        calculate_average([])
        assert False, "Should raise ValueError for empty list"
    except ValueError:
        pass

    try:
        calculate_average([1, "two", 3])
        assert False, "Should raise TypeError for non-numeric input"
    except TypeError:
        pass

    print("✓ All average tests passed")


def test_calculate_median():
    """Test median calculation with various inputs."""
    assert calculate_median([1, 2, 3, 4, 5]) == 3
    assert calculate_median([1, 2, 3, 4]) == 2.5
    assert calculate_median([5]) == 5
    assert calculate_median([3, 1, 2]) == 2

    # Test error case
    try:
        calculate_median([])
        assert False, "Should raise ValueError for empty list"
    except ValueError:
        pass

    print("✓ All median tests passed")


if __name__ == "__main__":
    # Run tests
    test_calculate_average()
    test_calculate_median()

    # Example usage
    data = [10, 20, 30, 40, 50]
    print(f"\nData: {data}")
    print(f"Average: {calculate_average(data)}")
    print(f"Median: {calculate_median(data)}")
