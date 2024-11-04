a=eval(input())
for i in a:
    if (type(a[i])==type(0) or type(a[i])==type(0.1)) and a[i]>=0 and a[i]<=100:
        print('{} {}'.format(i,a[i]))