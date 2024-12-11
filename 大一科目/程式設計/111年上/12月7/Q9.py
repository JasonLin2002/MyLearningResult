def fun(n):
    if x==1:
        for i in range(n+1):
            print(' '*(n-i)+'*'*(2*i-1))
        return
    elif x==2:
        for i in range(n+1):
            print(' '*(n-i)+'*'*(2*i-1))
        for i in range(n-1,0,-1):
            print(' '*(n-i)+'*'*(2*i-1))
        return
    elif x==3:
        print("*"*n)
        for i in range(n-2):
            print("*"," "*(n-4),"*")
        print("*"*n)
        return
if __name__=="__main__":
    n=int(input())
    x=int(input())
    fun(n)