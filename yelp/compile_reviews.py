#Author: Rahul Ram
#Date: 3/17/15


#!/bin/python
import json
import unicodedata



business_file = '/rahul_extra/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
review_file = '/rahul_extra/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'


def fetch_bid():
	'''
	Returns Business ID of all the restaurtants which come under restaurant cateogry
	'''
	bid = []
	fdata = open('./data/restaurant_categories.txt')
	rest_category = []
	for names in fdata:
		names = names.strip('\n')
		rest_category.append(names.lower())

	print "the restaurant categories are ",rest_category

	fbr = open(business_file,'r')
	for reviews in fbr:
		jl = json.loads(reviews)
		j_categories  = [str(i).lower() for i in jl['categories']]
		if set(j_categories) & set(rest_category):
			bid.append(str(jl['business_id']))
	return bid


#Returns True if the business id refers to restaturant names
def sanitize(json_line,label):
	jstr = json_line[label]
	jnorm = unicodedata.normalize('NFKD', jstr).encode('ascii','ignore')
	return jnorm


def main():
	fr = open(review_file,'r')
	f = open('restaurant_reviews_with_bid.txt' ,'a')

	blist = fetch_bid()

	print "this list of business ids are ",blist

	for line in fr:
		mdict  = {}
		jl = json.loads(line)
		cur_bid = sanitize(jl,'business_id')
		if cur_bid in blist:
			review_text = sanitize(jl, 'text')
			mdict['bid'] = cur_bid
			mdict['review'] = review_text
			json.dump(mdict, f,ensure_ascii=False)
	f.close()

if __name__ == '__main__':
	main()
