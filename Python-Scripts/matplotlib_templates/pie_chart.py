import matplotlib.pyplot as plt
import numpy as numpy

days = [1,2,3,4,5]

sleeping = [7,8,6,11,7]
eating = [2,3,4,3,2]
working = [7,8,7,2,2]
playing = [8,5,7,8,13]

slices = [7,2,2,13]
activities = ['sleeping', 'eating', 'working', 'playing']
colors = ['c', 'm', 'r', 'k']

plt.pie(slices,
        labels=activities,
        colors=colors,
        startangle=90,
        shadow=True,
        explode=(0,0.1,0,0),
        autopct='%1.1f%%'
            )

#plt.xlabel('nums')
#plt.ylabel('random nums')
plt.title('wassa duds\nhow yall doing')
#plt.legend()
plt.show()