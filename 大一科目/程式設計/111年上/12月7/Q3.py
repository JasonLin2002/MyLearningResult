def fun(a):
    a=list(a)
    b=0
    for i in a:
        if i !=' ':
            b+=1
    return b
def fun2(a):
    return len(a.split())
def fun3(a):
    return fun(a)/fun2(a)

if __name__=='__main__':
    a=input()
    print('{:.2f}'.format(fun3(a)))