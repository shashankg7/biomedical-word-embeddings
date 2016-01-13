biomedical-word-embeddings
==========================

http://jakerochlinmarcus.github.io/vector-representations.html

bash download_embeddings.sh
bash PubMed-and-PMC-w2v.sh

UMLS
====

install_umls.sh: downloads and installs the UMLS
create_umls_db.sh: creates a SQLite database containing a subset of the UMLS

Word embeddings
===============

download_embeddings.sh: downloads word embeddings trained on PubMed and PMC text (http://bio.nlplab.org/)

Analogies
=========

analogy.sql: exports a spreadsheet of term pairs with the relationship procedure_has_excised_anatomy
mrrel_vocab_excise.csv: a spreadsheet of term pairs with the relationship procedure_has_excised_anatomy
pairs.csv: cleaned up version of term pairs with the relationship procedure_has_excised_anatomy
create_analogies.py: produces analogies based on pairs.csv
analogies.txt: analogies based on pairs.csv

Install
=======

pip install -r requirements.txt
bash install_wvlib.sh
