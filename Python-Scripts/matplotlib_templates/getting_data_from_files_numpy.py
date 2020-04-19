import matplotlib.pyplot as plt
import numpy as np

x, y = np.loadtxt('ex', delimiter=',', unpack=True)

plt.plot(x,y, label='Data loaded from file')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Title Here')
plt.legend()
plt.show()