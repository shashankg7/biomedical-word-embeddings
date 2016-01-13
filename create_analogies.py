import pandas as pd
import numpy as np

if __name__ == '__main__':

	column1 = 'word1'
	column2 = 'word2'
	in_path = 'pairs.csv'
	out_path = 'analogies.txt'

	data = pd.read_csv(in_path)

	analogies = {}
	for rela in data['rela'].unique().tolist():
		print rela
		analogies[rela] = []
		pairs = data[data['rela'] == rela][[column1,column2]].drop_duplicates().reset_index(drop=True)
		for i in range(len(pairs)):
			for j in range(i+1, len(pairs)):
				a = pairs.iloc[i][column1]
				b = pairs.iloc[i][column2]
				c = pairs.iloc[j][column1]
				d = pairs.iloc[j][column2]
				if a != b and c != d and a != c and b != d:	
					analogy = [a, b, c, d]
					analogies[rela].append(analogy)

	with open(out_path, 'w') as f:
		for i, rela in enumerate(analogies.keys()):
			f.write(': ' + rela + '\n')
			for j, analogy in enumerate(analogies[rela]):
				f.write(' '.join(analogy))
				if j != (len(analogies[rela])-1):
					f.write('\n')
			if i != (len(analogies)-1):
				f.write('\n')
