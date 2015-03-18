# Running word2vec
0. `$ make`
1. `$ chmod +x yelp-make-vectors.sh`
2. `$ ./yelp-make-vectors.sh reviews.txt`

Here, reviews.txt is a raw text file containing each review in a single line  Remove punctuctinons, periods . Output of the file is 
* yelp_review_vocab.txt - containing word, word-cnt in each line seperated by space
* vectors.txt - containing word, vector each line seperated by space
