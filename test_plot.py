import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = fig.gca(projection='3d')
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)

r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)
ax.plot([1,2,22], [1,2,33], [1,2,44])
ax.legend()

plt.show()
