import sys
from random import random

rate = float(sys.argv[1])

for l in sys.stdin:
   if random() < rate:
        print l.rstrip()
