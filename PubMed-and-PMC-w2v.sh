python get_vocab.py PubMed-and-PMC-w2v.bin vocab.csv
umls.db < umls.sql # merge vocab.csv with the UMLS database
python reduce_vocab.py PubMed-and-PMC-w2v.bin PubMed-and-PMC-w2v_reduced.bin mrsty_vocab.csv # drop word embeddings out of the UMLS vocab 
python calc_tsne.py PubMed-and-PMC-w2v_reduced.bin tsne_PubMed-and-PMC-w2v.csv # project the word embeddings down to 2 dimensions
python calc_accuracy.py PubMed-and-PMC-w2v_reduced.bin analogies.txt accuracy_PubMed-and-PMC-w2v.csv 1 # evaluates the word embeddings based on an analogy task
python sample.py tsne_PubMed-and-PMC-w2v.csv mrsty_vocab.csv data_sample.csv # merges word embeddings with UMLS and takes a grid-based sample for graphing
