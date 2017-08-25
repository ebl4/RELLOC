import nltk
from nltk.corpus import PlaintextCorpusReader

corpus_root = '/Users/edson/Dropbox/Mestrado/NLTK'
wordlists = PlaintextCorpusReader(corpus_root, '.txt')
print(wordlists.fileids())

