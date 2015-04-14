import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


'''
Sample data in restaurant_count.txt
rest_id,value
rest_id,value
rest_id,value 
'''


x = []
with open('restaurant_count_unique.txt') as fr:
	for line in fr:
		x.append(float(line.split(',')[1]))


x.sort(reverse=True)
print len(x)
plt.style.use('ggplot')

# the histogram of the data
n, bins, patches = plt.hist(x, 100, range=[0, 1000], facecolor='green')

plt.ylabel('No of Food Related Words')
plt.title('Histogram of Food Related Words in Yelp Review')
plt.show()
