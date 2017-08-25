import nltk
import sys
reload(sys)
sys.setdefaultencoding("latin1")

file = open("ouro_preto", "r")

#corpus_root = '/Users/edson/Dropbox/Mestrado/NLTK'
#wordlists = PlaintextCorpusReader(corpus_root, '.txt')

article = file.read()

#sentence = wordlists.words()

for sentence in article.split('\n'):
	print(sentence.strip())

file.close()

