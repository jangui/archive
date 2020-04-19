import matplotlib.pyplot as plt

y = [i**2//(2**(i//2)) for i in range(1, 21, 2)]
x = [i for i in range(len(y))]

plt.scatter(x, y, label='rand data', color='k', marker='*', s=100)
plt.xlabel('nums')
plt.ylabel('random nums')
plt.title('wassa duds\nhow yall doing')
plt.legend()
plt.show()