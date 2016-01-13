import numpy as np
import pandas as pd
import gensim
from tsne import bh_sne
from optparse import OptionParser

if __name__ == '__main__':
	
	parser = OptionParser()
	(options, args) = parser.parse_args()
	assert len(args) == 2

	in_file = args[0]
	out_file = args[1]

	model = gensim.models.word2vec.Word2Vec.load_word2vec_format(in_file, binary=True)

	vectors = np.zeros((len(model.vocab), model.vector_size))
	words = model.vocab.keys()
	for i, key in enumerate(words):
		vectors[i,:] = model[key]
	
	vis_data = bh_sne(vectors)
	out = pd.DataFrame({'x': vis_data[:,0], 'y': vis_data[:,1], 'word': words})
	out.to_csv(out_file, index=False) 
