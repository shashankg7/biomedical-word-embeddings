import numpy as np
import pandas as pd
from optparse import OptionParser

import word2vec_util 
word2vec_util = reload(word2vec_util)

if __name__ == '__main__':

	parser = OptionParser()
	(options, args) = parser.parse_args()
	assert len(args) == 2

	in_file = args[0]
	out_file = args[1]

	vocab = word2vec_util.get_vocab(in_file) 
	data = pd.DataFrame({'term': vocab})
	data.to_csv(out_file, index=False, header=False)
