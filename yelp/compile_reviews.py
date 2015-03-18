
'''
Word dictionary building, word ambience. 
'''

#!/bin/python
import json
import unicodedata



def category(label):

	



def main():
	fr = open('yelp_academic_dataset_review.json','r')
	f = open('reviews_only.txt' ,'a')
	for line in fr:
		jl = json.loads(line)
		jstr = jl['text']
		jnorm = unicodedata.normalize('NFKD', jstr).encode('ascii','ignore')
		f.write(jnorm)
		f.write("\n\n")
	f.close()

if __name__ == '__main__':
	main()
