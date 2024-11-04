def count_regions(n):
    if n == 0:
        return 1
    else:
        previous_count = count_regions(n - 1)
        return previous_count + n

n = 4  
result = count_regions(n)
print(f"{n}條直線將平面分成最多的區域數是: {result}")