import csv

file_rating = '/rahul_extra/yelp_ml/w2vec/rest_ratings.txt'
file_nof_words = '/rahul_extra/yelp_ml/w2vec/restaurant_reviews_total_words.txt'
file_no_reviews = '/rahul_extra/yelp_ml/w2vec/rest_review_count.txt'
file_unique_food = '/rahul_extra/yelp_ml/w2vec/restaurant_count_unique.txt'
file_total_food = '/rahul_extra/yelp_ml/w2vec/restaurant_total_food_words.txt'




def create_dict(filename):
	d = {}
	with open(filename,'r') as f:
		for line in f:
			l = line.split(",")
			d[l[0]] = l[1]
	return d

dratings = create_dict(file_rating)
dnofw = create_dict(file_nof_words)
dnor = create_dict(file_no_reviews)
duf = create_dict(file_unique_food)
dtf = create_dict(file_total_food)

with open('finaldata.csv', 'w') as f:
	f.write('business_id,avg_ratings,total_no_of_words,total_reviews,unique_food_words,total_food_words'+"\n")
	for k in dratings:
		r = dratings[k].strip('\n')
		if dnofw.has_key(k):
			nofw = dnofw[k].strip('\n')
		else:
			nofw = 'None'
		
		if dnor.has_key(k):
			nor = dnor[k].strip('\n')
		else:
			nor = 'None'

		if duf.has_key(k):
			uf = duf[k].strip('\n')
		else:
			uf = 'None'

		if dtf.has_key(k):
			tf = dtf[k].strip('\n')
		else:
			tf = 'None'

		line = k +","+r+","+nofw+","+nor+","+uf+","+tf
		f.write(line+"\n")
