import matplotlib.pyplot as plt

y = [i**2//(2**(i//2)) for i in range(1, 20, 2)]
x = [i for i in range(len(y))]

plt.plot(x, y, label='rand data', color='k')
plt.xlabel('nums')
plt.ylabel('random nums')
plt.title('wassa duds\nhow yall doing')
plt.legend()
plt.show()
