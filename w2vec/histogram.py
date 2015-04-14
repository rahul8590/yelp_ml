import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


x = []
with open('restaurant_count.txt') as fr:
	for line in fr:
		x.append(float(line.split(',')[1]))



plt.style.use('ggplot')

# the histogram of the data
n, bins, patches = plt.hist(x, 100, range=[0, 8000], facecolor='green')

plt.ylabel('No of Food Related Words')
plt.title('Histogram of Food Related Words in Yelp Review')
plt.show()
