import numpy as np

a = []
b = []
c = 0
while True :
    d = int(input('First array: Input -9999 to end:'))
    if d == -9999 :
        break
    else :
        a.append(d)
c = 0
while True :
    d = int(input('Second array: Input -9999 to end:'))
    if d == -9999 :
        break
    else :
        b.append(d)

e = sum((a-np.mean(a))*(b-np.mean(b)))
f = np.sqrt(sum((a-np.mean(a))**2))
g = np.sqrt(sum((b-np.mean(b))**2))


print('pearson = {} / ({}{}) = {}'.format(e,f,g,(e/(f*g))))