import sys
import re
import multiprocessing as mp


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

def preprocess(ifile):
        frw = open('preprocess_restaurant.txt','w')
        thread_pool = mp.Pool(processes=2)
        for line in open(ifile, 'r'):
               count += 1
               wrd  = [w.lower() for w in line.strip().split()]
               if wrd == []: continue
               #wrds = [process(w) for w in wrd]
               wrds = thread_pool.map(process, wrd)
               fwline = ' '.join(wrds) 
               frw.write(fwline)
               frw.write("\n")
               #frw.flush()
        frw.close()
                     

if __name__ == '__main__':
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
  preprocess(sys.argv[1])

