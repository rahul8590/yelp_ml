#!/bin/sh

in_review_file=$1
./word2phrase -train ${in_review_file} -output yelp_review_p2.txt data-phrase.txt -threshold 200 -debug 2
./word2phrase -train yelp_review_p2.txt -output yelp_review_p3.txt data-phrase.txt -threshold 200 -debug 2
./word2phrase -train yelp_review_p3.txt -output yelp_review_p4.txt data-phrase.txt -threshold 200 -debug 2
./word2vec -train yelp_review_p4.txt -output vectors.txt -cbow 0 -size 100 -window 10 -negative 10 -hs 0 -sample 1e-4 -threads 15 -binary 0 -iter 3 -min-count 10 -save-vocab yelp_review_vocab.txt
