a=int(input())
b=float(input())
c=input()
d=input()

def fun():
    if d=='True':
        if c=='True':
            x=(a-20)*0.9
        else:
            x=(a-20)
    else:
        if c=='True':
            x=a*0.9
        else:
            x=a
    return int(x+round(x*b))

print(fun())