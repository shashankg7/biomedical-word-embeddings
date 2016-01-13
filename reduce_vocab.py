import numpy as np
import pandas as pd
from optparse import OptionParser

import word2vec_util 
word2vec_util = reload(word2vec_util)

if __name__ == '__main__':

	parser = OptionParser()
	(options, args) = parser.parse_args()
	assert len(args) == 3

	in_path = args[0]
	out_path = args[1]
	vocab_path = args[2]

	vocab = set(pd.read_csv(vocab_path)['term'].unique().tolist())

	model = word2vec_util.reduce_vocab(in_path, vocab)
	model.save_word2vec_format(out_path, binary=True)
