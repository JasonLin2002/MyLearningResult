y=int(input())
x=int(input())

def fun(x,y):
    if x<60 and y<90:
        return('Low')
    elif x<80 and y<120:
        return('Ideal')
    elif x<90 and y<140:
        return('Pre-high')
    elif x<100 and y<190:
        return('High')

print(fun(x,y))