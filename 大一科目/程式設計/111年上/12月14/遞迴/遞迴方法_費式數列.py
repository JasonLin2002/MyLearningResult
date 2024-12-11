def fuck(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fuck(n-1)+fuck(n-2)
if __name__=='__main__':
    n=int(input())
    print(fuck(n))

