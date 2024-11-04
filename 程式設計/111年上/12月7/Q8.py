x=eval(input())
def fun(x):
    a=0
    for i in range (len(x)):
        for j in range (5):
            a+=int(x[i][j])
    b=a/len(x)/5
    return '{:.2f}'.format(b)
print(fun(x))