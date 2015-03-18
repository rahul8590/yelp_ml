import sys

def process(wrd):
        new_wrd = []
        for s in wrd:
              if s.isalpha() or s.isdigit() or s == '-':
                   new_wrd.append(s) 
              else :
                   new_wrd.append(' ')
        return ''.join(new_wrd)

def preprocess(ifile):
        for line in open(ifile, 'r'):
               wrds = map(lambda w : w.lower(), line.strip().split())
               wrds = map(lambda w : process(w), wrds)
               print ' '.join(wrds) 
                     

if __name__ == '__main__':
       preprocess(sys.argv[1])


