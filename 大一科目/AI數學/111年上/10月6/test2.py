import matplotlib . pyplot as plt
import numpy as np

x=np.linspace(-2, 2, 100)
y=x**2
fig = plt.figure(figsize = (12, 7))


plt.title('Equation plot')

plt.xlabel('x axis' )
plt.ylabel('y axis' )

plt.plot(x, y, label ='Y = X^2' , color ='red', linewidth = 1)

plt.plot(x, 2 * y, label ='Y = 6 * X^2' , color ='yellow', linewidth = 1)


plt.grid(linestyle ='-')


plt.legend( )

plt.show ()