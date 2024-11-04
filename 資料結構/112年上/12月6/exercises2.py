def quick_sort(arr):
    """
    The Quick Sort function that implements the sorting algorithm using recursion.
    """
    if len(arr) <= 1:
        return arr

    else:
        pivot = arr[-1]
        smaller, greater = [], []

        for x in arr[:-1]:
            if x <= pivot:
                smaller.append(x)
            else:
                greater.append(x)

        return quick_sort(smaller) + [pivot] + quick_sort(greater)

example_arr = [33, 31, 4, 8, 12, 17, 51, 42, 3, 9]

sorted_arr = quick_sort(example_arr)
print(sorted_arr)