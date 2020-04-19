import matplotlib.pyplot as plt


x = [2,4,6,8,10]
y = [6,7,2,4,12]

x2 = [1,3,5,7,9]
y2 = [7,8,4,2,5]

plt.bar(x, y, label='Bars1', color='r')
plt.bar(x2, y2, label='bars2', color='c')

plt.xlabel('nums')
plt.ylabel('random nums')
plt.title('wassa duds\nhow yall doing')
plt.legend()
plt.show()
