import matplotlib.pyplot as plt
import numpy as np

def O_1(n):
    return n*(1/n)

def O_n(n):
    return n

def O_n2(n):
    return n**2

def O_n3(n):
    return n**3

def O_2n(n):
    return 2**n

def O_log2n(n):
    return np.log2(n)

def O_nlog2n(n):
    return np.log2(n)*n

x = np.linspace(0.1, 10, 1000)
plt.figure(figsize=(12, 8))

plt.plot(x, O_1(x), color="brown", label="O(1)")
plt.plot(x, O_n(x), color="blue", label="O(n)")
plt.plot(x, O_n2(x), color="orange", label="O(n^2)")
plt.plot(x, O_n3(x), color="pink", label="O(n^3)")
plt.plot(x, O_2n(x), color="red", label="O(2^n)")
plt.plot(x, O_log2n(x), color="green", label="O(n*log2(n))")
plt.plot(x, O_nlog2n(x), color="purple", label="O(log2(n))")

plt.title("Big O")
plt.xlabel("x")
plt.ylabel("y")

plt.ylim(-1, 10)
plt.legend()
plt.show()
