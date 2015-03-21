#!/usr/bin/env python
import sys, re, time, pp
import multiprocessing as mp
from itertools import izip_longest, islice
from joblib import Parallel, delayed
import time

#================Regex Initializtions============================================#

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
common_re   = re.compile(r"^(haven't|shouldn't|can't|couldn't|wouldn't|won't|don't|that's|i'm|it's|i've|i'll|here's)$")
re_patterns = (money_re, phone_re, weekday_re, weekend_re, year_re)
re_repl     = ("MONEY",  "PHONE",  "WEEKDAY",  "WEEKEND",  "YEAR") 
patterns    = zip(re_patterns, re_repl)

#================Regex Initializtions Ends==========================================#


def process_word(wrd):
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
	      elif prev_ch: 
	             new_wrd.append(' ')
	             prev_ch = False
	return ''.join(new_wrd)

def process_line(line):
        wrds = [w for w in [process_word(wrd) for wrd in line.split()] if len(w) > 0] 
	return ' '.join(wrds)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)

def main(ifile):
	ofptr = open('joblib_preprocess_output.txt', 'w')
	ifptr = open(ifile, 'r')
        ''' process 10000 lines in parallel '''
        t0 = time.time()
        for multi_lines in grouper(ifptr, 5000):
                lines  = [line.strip() for line in multi_lines if line is not None]
                if lines == []: break 
                processed_lines = Parallel(n_jobs=10)(delayed(process_line)(line) for line in lines)
	        for result in processed_lines:
                     ofptr.write(result)
                     ofptr.write("\n")
	ofptr.close()
        print "tota time", time.time() - t0, " secs"
		

if __name__ == '__main__':
	main(sys.argv[1])


'''Sample fast_preprocess_output

Starting Parallel Python with 4 workers
job completed
Job execution statistics:
 job count | % of all jobs | job time sum | time per job | job server
      2658 |        100.00 |     276.1100 |     0.103879 | local
Time elapsed since server creation 301.073426962
0 active tasks, 4 cores

None

Filesize Difference seems huge
-rw-rw-r-- 1 rahul rahul 597M Mar 20 16:34 fast_preprocess_output.txt
-rw-rw-r-- 1 rahul rahul 613M Mar 18 20:34 preprocess_restaurant.txt
'''
