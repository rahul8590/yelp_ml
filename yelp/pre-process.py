import sys
import re

## replace all costs by MONEY
## replace all year by YEAR
## take care of wasn't haven't havenot wasnot -> wasn't haven't

money_re = re.compile('|'.join([
              r'^\$(\d*\.\d{1,2,3)$',
              r'^\$(\d+)$']))

def process(wrd):
        if money_re.match(wrd):
            return wrd
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
               wrds = map(lambda w : w.lower(), line.strip().split())
               wrds = map(lambda w : process(w), wrds)
               print ' '.join(wrds) 
                     

if __name__ == '__main__':
       preprocess(sys.argv[1])


