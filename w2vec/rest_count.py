#!/bin/python
import json
import sys
dcount = {}
file_sorted = '/rahul_extra/yelp_ml/yelp/data/plabel_v2_sorted.csv'
file_review = '/rahul_extra/yelp_ml/w2vec/yelp_review_p4.txt'
wl = {}

#Returns True if the business id refers to restaturant names
def sanitize(json_line,label):
	jstr = json_line[label]
	jnorm = unicodedata.normalize('NFKD', jstr).encode('ascii','ignore')
	return jnorm


def calc_lw(text):
	lw = []
	for i in text.split(' '):
		if i in wl:
			lw.append(i)
	return lw


with open(file_sorted, 'r') as flabel:
	for line in flabel:
		l = line.split(",")
		if l[1] > 0.5:
			wrd = l[0].strip('-')
			wl[wrd] = 0


#print "the word list is completed " , wl ,len(wl)


with open(file_review,'r') as fr:
	for line in fr:
		try:
			dl = json.loads(line)
		except:
			print line 
			continue
		if dcount.has_key(str(dl['bid'])):
			sl = dcount[str(dl['bid'])]
		else:
			sl = []
		
		ires = calc_lw(str(dl['review']))
		for i in ires:
			sl.append(i)
		dcount[str(dl['bid'])] = sl


		#dcount[str(dl['bid'])] = dcount.get(str(dl['bid']),0) 
		#print 	dl['bid'] , dcount[str(dl['bid'])]



with open('restaurant_count_unique.txt','a') as fc:
	for k in dcount:
		fc.write(str(k)+","+str(len(set(dcount[k])))+"\n")
		




 