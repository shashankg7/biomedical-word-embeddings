import pandas as pd
import numpy as np
import pdb
import pylab as pl
import simplejson as json

def analyze_accuracy():

	topn = 5
	data = pd.read_csv('accuracy_PubMed-and-PMC-w2v.csv')
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

	out = data[['is_correct_0','is_correct_1','is_correct_2','is_correct_3','is_correct_4','is_procedure']].mean()

	return out

if __name__ == '__main__':

	out = analyze_accuracy()
	with open('accuracy.json', 'w') as fout:
		fout.write(out.to_json())

