import sys
import re
import multiprocessing as mp

def process(wrd):
        if wrd in donot_process_wrds:
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

def preprocess(ifile):
        for line in open(ifile, 'r'):
               wrd = [w.lower() for w in line.strip().split()]
               wrds = thread_pool.map(process,wrd)
               print ' '.join(wrds) 
                     

if __name__ == '__main__':
  ## replace all year by YEAR
  ## take care of wasn't haven't havenot wasnot -> wasn't haven't
  money_re  = re.compile('|'.join([
                          r'\$(\d*\.\d{1,2,3,4})',   ## $.50000, $.34
                          r'\$(\d+)',               ## $500, $300
                          r'\$(\d+\.\d{1,2,3,4})']))  #3 $5.33, $3.2.2
  phone_re  = re.compile('|'.join([
                          r'(\d(\s|-)){0,1}\d{3}(\s|-)\d{3}-\d{4}',             ## 765-413-3419
                          r'(\d(\s|-)){0,1}\(\d{3}\)(\s|-)\d{3}-\d{4}' ]))      ## (765)-413-3419, (765) 413-3419
  #month_re   = re.compile(r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec", re.I)
  #weekday_re = re.compile(r"Mon|Tue|Tues|Wed|Thu|Thurs|Fri", re.I)
  weekend_re = re.compile(r"Saturday|Sunday", re.I)
  year_re    = re.compile(r"^(19|20)\d{2}s*")
  num_re     = re.compile(r"^(.|!|\s)*\d+(.|!|\s)*$")
  re_patterns = (money_re, phone_re, weekend_re, year_re, num_re)
  re_repl     = ("MONEY", "PHONE", "WEEKEND", "YEAR", "NUMBER") 
  patterns = zip(re_patterns, re_repl)
  donot_process_wrds = {"haven't" : 1, "shouldn't" : 1, "won't" : 1, "don't" : 1}
  thread_pool = mp.Pool(processes=4)
  preprocess(sys.argv[1])


