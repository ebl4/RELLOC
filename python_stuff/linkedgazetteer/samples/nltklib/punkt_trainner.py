import nltk.tokenize.punkt
from nltk.corpus import floresta
import pickle
import codecs
tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
text = codecs.open("someplain.txt","r","utf8").read()
tokenizer.train(text)
out = open("someplain.pk","wb")
pickle.dump(tokenizer, out)
out.close()