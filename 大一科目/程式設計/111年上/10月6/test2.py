a=int(input())
b=int(input())
c=int(input())
max=0

if a>b:
    if a>c:
        max=a
    else:
        max=c
elif b>c:
    max=b
else:
    max=c
print(int(max))