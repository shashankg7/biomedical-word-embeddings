sudo apt-get update
sudo apt-get install unzip python-numpy python-scipy python-pandas python-pip libblas-dev libatlas-dev liblapack-dev libatlas-base-dev
sudo pip install gensim

python convert_wvlib.py # requires a lot of memory. ran it on a r3.2xlarge AWS instance
python reduce_vocab.py PubMed-and-PMC-ri.bin PubMed-and-PMC-ri_reduced.bin mrsty_vocab.csv
python calc_tsne.py PubMed-and-PMC-ri_reduced.bin tsne_PubMed-and-PMC-ri.csv
python calc_accuracy.py PubMed-and-PMC-ri_reduced.bin analogies.txt accuracy_PubMed-and-PMC-ri.csv 1 
