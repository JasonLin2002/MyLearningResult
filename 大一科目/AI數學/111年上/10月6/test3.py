from cProfile import label
import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(-np.pi,np.pi,1000)
y=np.sin(x)
y2=np.cos(x)

fig= plt.figure(figsize=(12,7))

plt.title('Equation plot')

plt.xlabel('x axis')
plt.xlabel('y axis')

plt.plot(x,y,label='Y=sin(x)',color='red',linewidth=1)
plt.plot(x,y2,label='Y=cos(x)',color='blue',linewidth=1)

plt.grid(linestyle='-')
plt.legend()
plt.show()