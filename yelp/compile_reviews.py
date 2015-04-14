#!/bin/python
#Author: Rahul Ram
#Date: 3/17/15

import json
import unicodedata
import sys
import re
import multiprocessing as mp

business_file = '/rahul_extra/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json'
review_file = '/rahul_extra/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json'

money_re    = re.compile('|'.join([
                          r'\$(\d*\.\d{1,2,3,4})',   ## $.50000, $.34
                          r'\$(\d+)',               ## $500, $300
                          r'\$(\d+\.\d{1,2,3,4})']))  #3 $5.33, $3.2.2
phone_re    = re.compile('|'.join([
                      r'(\d(\s|-)){0,1}\d{3}(\s|-)\d{3}-\d{4}',             ## 765-413-3419
                      r'(\d(\s|-)){0,1}\(\d{3}\)(\s|-)\d{3}-\d{4}' ]))      ## (765)-413-3419, (765) 413-3419
weekday_re  = re.compile(r"^(Monday|Tues|Tuesday|Wednesday|Thurs|Thrusday|Friday)$", re.I)
weekend_re  = re.compile(r"^(Saturday|Sunday)$", re.I)
year_re     = re.compile(r"^(19|20)\d{2}s*")
#num_re      = re.compile("|".join([
#                        r"^(.|!|\s)*\d+(.|!|\s)*$",
#                        r"^(\d+)$"]))
common_re   = re.compile(r"^(haven't|shouldn't|can't|won't|don't|that's|i'm|it's|i've|i'll|here's)$")
re_patterns = (money_re, weekday_re, weekend_re, year_re , phone_re)
re_repl     = ("MONEY", "PHONE", "WEEKDAY", "WEEKEND", "YEAR", "NUMBER") 
patterns    = zip(re_patterns, re_repl)

def process(wrd):
        if common_re.match(wrd):
            return wrd
        for re_pattern, repl in patterns:
                if re_pattern.match(wrd):
                      wrd = re_pattern.sub(repl, wrd)
                      break
        new_wrd = []
        prev_ch = False ## was previous char space ?
        for s in wrd:
              if s.isalpha() or s.isdigit() or s  == '-':
                   new_wrd.append(s) 
                   prev_ch = True
              else :
                   if prev_ch: 
                     new_wrd.append(' ')
                     prev_ch = False
        return ''.join(new_wrd)


def line_sanitize(line):
	#thread_pool = mp.Pool(processes=2)
	wrd  = [w.lower() for w in line.strip().split()]
	if wrd == []: return None
	wrds = [process(i) for i in  wrd]
	return wrds

def fetch_rbid():
	bid = []
	with open('/rahul_extra/yelp_ml/yelp/rest_bid.txt') as fr:
		for ids in fr:
			ids = ids.strip('\n')
			bid.append(str(ids))
	return bid



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

	blist = fetch_rbid()

	print "this list of business ids are ",len(blist)

	for line in fr:
		mdict  = {}
		jl = json.loads(line)
		cur_bid = sanitize(jl,'business_id')
		if cur_bid in blist:
			review_text = sanitize(jl, 'text')
			rtext = line_sanitize(review_text)
			if rtext == None: continue
			mdict['bid'] = cur_bid
			mdict['review'] = ' '.join(rtext)
			json.dump(mdict, f,ensure_ascii=False)
			f.write("\n")
	f.close()

if __name__ == '__main__':
	main()
