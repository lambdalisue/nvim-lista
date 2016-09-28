import os
import sys
from functools import reduce

rep = reduce(lambda x, f: f(x), [os.path.dirname] * 4, __file__)
lib = os.path.join(rep, 'rplugin', 'python3')
sys.path.insert(0, lib)
