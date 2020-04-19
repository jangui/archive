import matplotlib.pyplot as plt

population_ages = [22,55,66,77,13,6,34,65,23,58,36,94,38,73,35,86,34,87,56,5,99,101,111,121,45,56,67,78,89,90,21,32,43,54,65,76,87,98]
bins = [0,10,20,30,40,50,60,70,80,90,100,110,120,130]

plt.hist(population_ages, bins, histtype='bar', rwidth=0.8)

plt.xlabel('nums')
plt.ylabel('random nums')
plt.title('wassa duds\nhow yall doing')
plt.legend()
plt.show()