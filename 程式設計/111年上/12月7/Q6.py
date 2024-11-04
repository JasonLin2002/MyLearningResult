x=int(input())
y=float(input())
z=int(input())

def fun1():
    return '{:.2f}'.format(x+x*y)
def fun2():
    return '{:.2f}'.format(x+x*y-z)
print(fun1())
print(fun2())