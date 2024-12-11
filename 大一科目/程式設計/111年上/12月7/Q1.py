def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

n = int(input())

a=0

for i in range(2, n + 1):
    i_is_prime = is_prime(i)
    if i_is_prime:
        a+=i
print(a)