import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.cm as cm
import random
import pdb
from optparse import OptionParser

def get_data(tsne_path, semantic_path):
	tsne = pd.read_csv(tsne_path)
	semantic_types = pd.read_csv(semantic_path)
	semantic_types.columns = ['cui','word','semantic_type']

	data = pd.merge(tsne, semantic_types, on='word')
	
	return data

def add_zones(data, num_steps):

	x_min = np.min(data['x'])
	x_max = np.max(data['x'])

	y_min = np.min(data['y'])
	y_max = np.max(data['y'])

	x = np.arange(x_min, x_max, (x_max - x_min)/num_steps)[0:num_steps]
	x[num_steps-1] = x_max

	y = np.arange(y_min, y_max, (y_max - y_min)/num_steps)[0:num_steps]
	y[num_steps-1] = y_max

	data.loc[:, 'zone'] = np.nan
	k = 0
	for i in range(len(x)-1):
		print i
		for j in range(len(y)-1):
			z = ((data['x'] >= x[i]) & (data['x'] <= x[i+1]) & (data['y'] >= y[j]) & (data['y'] <= y[j+1]))
			data.loc[z, 'zone'] = k
			k += 1	

	return x, y, data

def plot_zones(data):

	pl.scatter(data['x'], data['y'], color='blue')
	zones = data['zone'].unique().tolist()
	colors = iter(cm.rainbow(np.linspace(0, 1, len(zones))))
	for zone in zones:
		pl.scatter(data['x'][data['zone'] == zone], data['y'][data['zone'] == zone], color=next(colors))
	pl.show()

def plot_sample(data):

	pl.figure()
	pl.subplot(211)	
	pl.scatter(data['x'][data['sample'] == 1], data['y'][data['sample'] == 1], color='red')
	pl.subplot(212)
	pl.scatter(data['x'], data['y'])
	pl.show()

def add_sample(data):

	p = 0.1
	zones = data['zone'].unique().tolist()

	data.loc[:, 'sample'] = np.nan

	print len(zones)
	for i, zone in enumerate(zones):
		print i

		z = (data['zone'] == zone)
		num_1 = np.ceil(p*np.sum(z))
		num_0 = np.sum(z) - num_1
		samp = [1]*num_1 + [0]*num_0
		random.shuffle(samp) 
		data.loc[z, 'sample'] = samp 

	return data

if __name__ == '__main__':

	parser = OptionParser()
	(options, args) = parser.parse_args()
	assert len(args) == 3

	tsne_path = args[0]
	semantic_path = args[1]
	out_path = args[2]

	data = get_data(tsne_path, semantic_path)
	x, y, data_zones = add_zones(data, num_steps=20)
	data_samp = add_sample(data_zones)	
	data_samp[data_samp['sample'] == 1].to_csv(out_path, index=False)
