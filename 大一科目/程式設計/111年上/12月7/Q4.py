def fun(a,b):
    for i in a:
        flag=False
        for j in b:
            if i == j:
                flag = True
        if flag ==False:
            break
    return flag
if __name__=='__main__':
    a=input()
    b=input()
    print(fun(a,b))