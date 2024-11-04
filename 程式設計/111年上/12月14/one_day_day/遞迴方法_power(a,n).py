def fun(a,b):
    if b==1:
        return a
    else:
        return a*fun(a,b-1) 
def you(a,b):
    if b%2==0:
        return you(a,b/2)*you(a,b/2)
    elif b==1:
        return a
    else:
        return a*you(a,b-1)
if __name__=='__main__':
    a,b=map(int,input().split())
    print(fun(a,b))
    print(you(a,b))
    