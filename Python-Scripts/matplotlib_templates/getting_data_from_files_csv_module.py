import matplotlib.pyplot as plt
import csv
import numpy as np

x = []
y = []

with open('ex', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))

plt.plot(x, y, label='Loaded From File')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Title Here')
plt.legend()
plt.show()