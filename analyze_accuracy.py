import pandas as pd
import numpy as np
import pdb
import pylab as pl
import simplejson as json

def analyze_accuracy(fname):

	topn = 5
	data = pd.read_csv(fname)
	umls = pd.read_csv('mrrel_vocab_excise.csv')
	umls.columns = ['cui1','cui2','anatomy','procedure','rela']
	procedures = set(umls['procedure'].tolist())

	data['is_procedure'] = map(lambda x: (x in procedures) or x.endswith('tomy'), data['guess_0'])
	for i in range(topn):
		data['status_'+str(i)] = (data['guess_'+str(i)] == data['analogy_3'])
	for i in range(topn):
		data['is_correct_'+str(i)] = 0
		for j in range(i+1):
			data['is_correct_'+str(i)] += data['status_'+str(j)]

	out = data[['is_correct_0','is_correct_1','is_correct_2','is_correct_3','is_correct_4','is_procedure']].mean().reset_index()

	return out

def get_label(x):

	if x == 'is_correct_0':
		return 'Best guess'
	elif x == 'is_correct_1':
		return 'Top 2'
	elif x == 'is_correct_2':
		return 'Top 3'
	elif x == 'is_correct_3': 
		return 'Top 4'
	elif x == 'is_correct_4':
		return 'Top 5'
	elif x == 'is_procedure':
		return 'Guessed a procedure'

if __name__ == '__main__':

	w2v = analyze_accuracy('accuracy_PubMed-and-PMC-w2v.csv')
	ri = analyze_accuracy('accuracy_PubMed-and-PMC-ri.csv')

	chart_data = []
	chart_data.append({"key": "random_indexing", "values": [{"x": get_label(x), "y": 100*y} for x, y in ri.values]})
	chart_data.append({"key": "word2vec", "values": [{"x": get_label(x), "y": 100*y} for x, y in w2v.values]})

	with open('accuracy.json', 'w') as fout:
		fout.write(json.dumps(chart_data))

