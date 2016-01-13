import gensim
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import pdb

class Vocab(object):
	"""A single vocabulary item, used internally for constructing binary trees (incl. both word leaves and inner nodes)."""
	def __init__(self, **kwargs):
		self.count = 0
		self.__dict__.update(kwargs)

	def __lt__(self, other):  # used for sorting in a priority queue
		return self.count < other.count

	def __str__(self):
		vals = ['%s:%r' % (key, self.__dict__[key]) for key in sorted(self.__dict__) if not key.startswith('_')]
		return "<" + ', '.join(vals) + ">"

def get_vocab(path, num_lines=None, verbose=True):
	
	vocab = []
	with gensim.utils.smart_open(path, 'rb') as fin:
		header = fin.readline()
		vocab_size, layer1_size = map(int, header.split())
		binary_len = np.dtype(np.float32).itemsize * layer1_size

		if verbose:
			print vocab_size
		for line_no in xrange(vocab_size):
			if verbose:
				if (line_no % 100000) == 0:
					print line_no

			word = []
			while True:
				ch = fin.read(1)

				if ch == ' ':
					word = ''.join(word)
					break

				if ch != '\n':  # ignore newlines in front of words (some binary files have newline, some not)
					word.append(ch)

			vocab.append(word)				
			fin.seek(binary_len, 1)

			if num_lines is not None:
				if line_no == num_lines:
					break

	return vocab

def reduce_vocab(path, vocab=None, num_lines=None, norm_only=True, verbose=True):

	assert type(vocab) == type(set([])) or vocab == None

	counts = None
	with gensim.utils.smart_open(path, 'rb') as fin:
		header = fin.readline()
		full_vocab_size, layer1_size = map(int, header.split())
		if vocab is None:
			vocab_size = full_vocab_size
		else:
			vocab_size = len(vocab)
		result = Word2Vec(size=layer1_size)
		result.syn0 = np.zeros((vocab_size, layer1_size), dtype=np.float32)
		binary_len = np.dtype(np.float32).itemsize * layer1_size

		word_no = 0
		if verbose:
			print full_vocab_size
		for line_no in xrange(full_vocab_size):
			if verbose:
				if (line_no % 100000) == 0:
					print line_no

			word = []
			while True:
				ch = fin.read(1)

				if ch == ' ':
					word = ''.join(word)
					break

				if ch != '\n':  # ignore newlines in front of words (some binary files have newline, some not)
					word.append(ch)

			if (vocab is None) or (word in vocab):
				if counts is None:
					result.vocab[word] = Vocab(index=word_no, count=vocab_size - word_no)
				elif word in counts:
					result.vocab[word] = Vocab(index=word_no, count=counts[word])
				else:
					result.vocab[word] = Vocab(index=word_no, count=None)
				
				result.index2word.append(word)
				result.syn0[word_no] = np.fromstring(fin.read(binary_len), dtype=np.float32)
				word_no += 1
			else:
				fin.seek(binary_len, 1)

			if num_lines is not None:
				if line_no == num_lines:
					break

	result.init_sims(norm_only)
	result.syn0.resize((len(result.vocab), result.vector_size), refcheck=False)
	result.syn0norm.resize((len(result.vocab), result.vector_size), refcheck=False)
	return result
