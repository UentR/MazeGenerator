import matplotlib.pyplot as plt
from matplotlib import cm, use, colors
from matplotlib.ticker import LinearLocator
import numpy as np

use('Qt5Agg')

L = input()
while L not in ['T', 'O']:
    L = input("Retry with T or O:\n")

import json
with open(f'data/Out{L}.json') as X:
    data1 = json.load(X)
with open(f"data/Out2{L}.json") as X:
    data2 = json.load(X)

fig, ax = plt.subplots()

ax.plot(data1.keys(), data1.values(), c='r', label="Old")
ax.plot(data2.keys(), data2.values(), c='g', label='New')

ax.axes.get_xaxis().set_visible(False)

plt.show()

'''
fig, ax = plt.subplots(subplot_kw={'projection': "3d"})

import json
with open('Out.json') as X:
    data = json.load(X)
    
_X = np.arange(1, len(data)+1, 1)
_Y = np.arange(1, len(data)+1, 1)
X, Y = np.meshgrid(_X,_Y)
Z = np.array([[0]*len(data)]*len(data), ndmin=2)
max = 0
for x in _X:
    for y in _Y:
        t = data[str(x)][str(y)]
        if max < t < 3*10**6:
            max = t
        Z[x-1][y-1] = t


Z2 = np.power((X+Y), 2)

# surf = ax.plot_surface(X, Y, Z2, cmap=cm.RdYlGn, linewidth=0, antialiased=True)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.set_zlim(0, max)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
'''
