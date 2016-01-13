import gensim
import pdb
import pandas as pd
import numpy as np
from optparse import OptionParser

def read_analogies(path):
	analogies = {}
	with open(path, 'r') as f:
		for line in f:
			if line.find(':') != -1:
				rela = line.split(' ')[1].strip()
				analogies[rela] = []
			else:
				analogies[rela].append(line.strip().split(' '))
	return analogies

def accuracy(model, analogies, topn, lower):

	columns = ['rela']
	for i in range(4):
		columns.append('analogy_'+str(i))
	for i in range(topn):
		columns.append('guess_'+str(i))
	columns.append('status')

	out = {}
	for column in columns:
		out[column] = []

	for rela in analogies.keys():
		print rela
		print len(analogies[rela])
		for k, analogy in enumerate(analogies[rela]):
			if k % 100 == 0:
				print k
			
			in_vocab = True
			for word in analogy:
				if model.vocab.has_key(word) == False:
					in_vocab = False
					break
	
			if in_vocab == True:
				results = model.most_similar(positive=[analogy[1], analogy[2]], negative=[analogy[0]], topn=topn)
				if lower == True:
					results = [result[0].lower() for result in results]
				else:
					results = [result[0] for result in results]
	
				out['rela'].append(rela)
				for i in range(4):
					out['analogy_'+str(i)].append(analogy[i])
				for i in range(topn):
					out['guess_'+str(i)].append(results[i])
				out['status'].append((results[0] == analogy[3]))		

	out = pd.DataFrame(out)	
	return out[columns]

if __name__ == '__main__':

	parser = OptionParser()
	(options, args) = parser.parse_args()
	assert len(args) == 4

	vec_path = args[0]
	analogy_path = args[1]
	out_path = args[2]
	lower_int = int(args[3])
	if lower_int == 1:
		lower = True
	else:
		lower = False

	model = gensim.models.Word2Vec.load_word2vec_format(vec_path, binary=True)
	analogies = read_analogies(analogy_path)
	out = accuracy(model, analogies, topn=5, lower=lower)
	out.to_csv(out_path, index=False)
