import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

list=['發病日','確定病例數']

def pred(x, w):
    return np.matmul(x, w)

data = pd.read_csv('Age_County_Gender_day_19Cov(1).csv')
x_data = np.array(data[['發病日']])
yt = np.array(data[['確定病例數']])
x = np.insert(x_data, 0, 1.0, axis=1)
M = x.shape[0]
D = x.shape[1]
iters = 50000
alpha = 0.0
w = np.ones(D)
history = np.zeros((0, 2))

for k in range(iters):
    yp = pred(x, w)
    yd = yp - yt[:,0]
    w = w - alpha * (x.T @ yd) / M
    if k % 100 == 0:
        loss = np.mean(yd ** 2) / 2
        history = np.vstack((history, np.array([k, loss])))
        print(f'iter {k} \t loss: {loss}')

xall = x[:, 1].ravel()
x1 = np.array([[1, xall.min()], [1, xall.max()]])
yl = pred(x1, w)

plt.figure(figsize=(6, 6))
plt.scatter(x[:,1], yt, s=10, c='b')
plt.xlabel('Day of onset', fontsize=14)
plt.ylabel('Confirmed case', fontsize=14)

plt.xticks([401,501,601,701,801,901],
            ['4/1', '5/1', '6/1', '7/1', '8/1', '9/1'])

plt.plot(x1[:, 1], yl, c='k')
plt.show()

plt.plot(history[1:,0], history[1:,1])
plt.xlabel('Iteration', fontsize=14)
plt.ylabel('Loss', fontsize=14)
plt.show()