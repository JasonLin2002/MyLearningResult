from turtle import color
import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(-np.pi,np.pi,1000,endpoint=True)
Sin_y=np.sin(x)
Cos_y=np.cos(x)
plt.figure()
plt.plot(x,Sin_y,color='red',linewidth=1.0,linestyle="-",label="Sin")
plt.plot(x,Sin_y,color='blue',linewidth=1.0,linestyle="-",label="Cos")
plt.legend(loc='upper left')
plt.show()