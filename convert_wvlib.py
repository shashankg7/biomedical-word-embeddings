import sys

sys.path.insert(0, "wvlib-master/")

import wvlib

vec = wvlib.load('PubMed-and-PMC-ri.tar.gz')
vec.save_bin('PubMed-and-PMC-ri.bin')
