class MergeSort:
    @staticmethod
    def merge_sort_asc(A, p, r):
        if p < r:
            q = (p + r) // 2
            MergeSort.merge_sort_asc(A, p, q)
            MergeSort.merge_sort_asc(A, q + 1, r)
            MergeSort.merge(A, p, q, r)

    @staticmethod
    def merge_sort_desc(A, p, r):
        if p < r:
            q = (p + r) // 2
            MergeSort.merge_sort_desc(A, p, q)
            MergeSort.merge_sort_desc(A, q + 1, r)
            MergeSort.merge_desc(A, p, q, r)

    @staticmethod
    def merge(A, p, q, r):
        n_L = q - p + 1
        n_R = r - q
        L = [0] * n_L
        R = [0] * n_R

        for i in range(n_L):
            L[i] = A[p + i]
        for j in range(n_R):
            R[j] = A[q + j + 1]

        i = j = 0
        k = p

        while i < n_L and j < n_R:
            if L[i] <= R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
            k += 1

        while i < n_L:
            A[k] = L[i]
            i += 1
            k += 1

        while j < n_R:
            A[k] = R[j]
            j += 1
            k += 1

    @staticmethod
    def merge_desc(A, p, q, r):
        n_L = q - p + 1
        n_R = r - q
        L = [0] * n_L
        R = [0] * n_R

        for i in range(n_L):
            L[i] = A[p + i]
        for j in range(n_R):
            R[j] = A[q + j + 1]

        i = j = 0
        k = p

        while i < n_L and j < n_R:
            if L[i] >= R[j]:
                A[k] = L[i]
                i += 1
            else:
                A[k] = R[j]
                j += 1
            k += 1

        while i < n_L:
            A[k] = L[i]
            i += 1
            k += 1

        while j < n_R:
            A[k] = R[j]
            j += 1
            k += 1

import random
number = [random.randint(0, 100) for i in range(10)]

MergeSort.merge_sort_asc(number, 0, len(number) - 1)
print("小到大:", number)

MergeSort.merge_sort_desc(number, 0, len(number) - 1)
print("大到小:", number)
