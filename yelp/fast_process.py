#!/usr/bin/env python
import sys, re, time, pp
import multiprocessing as mp
from itertools import izip_longest


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
#num_re      = re.compile("|".join([
#                        r"^(.|!|\s)*\d+(.|!|\s)*$",
#                        r"^(\d+)$"]))
common_re   = re.compile(r"^(haven't|shouldn't|can't|won't|don't|that's|i'm|it's|i've|i'll|here's)$")
re_patterns = (money_re, weekday_re, weekend_re, year_re , phone_re)
re_repl     = ("MONEY", "PHONE", "WEEKDAY", "WEEKEND", "YEAR", "NUMBER") 
patterns    = zip(re_patterns, re_repl)

#================Regex Initializtions Ends==========================================#


def process(wrd,common_re,patterns):
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

def lprocess(lwords,common_re,patterns):
	pstr = ''
	for wrd_str in lwords:
		for wrd in wrd_str.split(' '):
			pstr += process(wrd,common_re,patterns)
	return pstr

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def main(ifile):
	ppservers = ()
	job_server = pp.Server(ppservers=ppservers)
	print "Starting Parallel Python with", job_server.get_ncpus(), "workers"
	frw = open('fast_preprocess_output.txt', 'w')
	with open(ifile,'r') as myfile:
		for multi_lines in grouper(myfile, 2000):
			ml = [line.strip() for line in multi_lines if line != None]
			if ml == []: continue
			job = job_server.submit(lprocess,(ml,common_re,patterns),(process,))
			result = job()
			frw.write(result + "\n")
	frw.close()
	print "job completed"
	print job_server.print_stats()
		

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
