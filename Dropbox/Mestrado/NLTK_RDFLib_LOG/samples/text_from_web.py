import nltk, re

import tkinter as tk
#from nltk import DefaultTagger, UnigramTagger, BigramTagger
from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk.corpus import mac_morpho
from bs4 import BeautifulSoup
import urllib.request


def all_childs(soup):
	for x in soup.body.childGenerator():
		print (x)

def formatText(trashs, text):
	for trash in trashs:
		text.replace(trash, "")
		return text


def textFromSoup(soup):
	text = soup.body.get_text()
	return text
	#return re.findall(r'<script>(.*?)</script>', text)

#train_texts_ids = mac_morpho.fileids()
#train_text = mac_morpho.raw("ag94ab12.txt")
#tsents = mac_morpho.tagged_sents()
#train = tsents[1000:]
#test = tsents[:100]


url0 = "https://en.wikipedia.org/wiki/Ouro_Preto"
#url = "https://en.wikipedia.org/wiki/New_York_City"
url = "https://economia.uol.com.br/ao-vivo/2017/08/01/direto-da-bolsa.htm"
response = urllib.request.urlopen(url)
html = response.read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')
text = ""

#print(soup.prettify())

for parag in soup("p"):
	text += (parag.get_text())

#print(text)

# tagger0 = DefaultTagger('NN')
# tagger1 = UnigramTagger(train, backoff=tagger0)
# tagger2 = BigramTagger(train, backoff=tagger1)

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#tagger = nltk.data.load('taggers/portuguese.pickle')
#chunker = nltk.data.load('chunkers/portuguese.pickle')

sents = sent_tokenizer.tokenize(text)


#print(taggedSent)

# Process the content for a nltk subroutine
# such as sentence chunk
def process_content_chunk():
	try:
		for i in sents:
			words = word_tokenize(i)
			tagged = nltk.pos_tag(words)

			chunkGram = r"""Chunk: {<NNP>*<RB.?>*<VB.?>*<NNP>+<NN>?}"""
			chunkParser = nltk.RegexpParser(chunkGram)
			chunked = chunkParser.parse(tagged)

			chunked.draw()
	except Exception as e:
		print(str(e))


def process_content():
	try:
		for i in sents:
			words = word_tokenize(i)
			tagged = nltk.pos_tag(words)

			nameEnt = nltk.ne_chunk(tagged)
			#IN = re.compile(r'.*\bin\b(?!\b.+ing)')
			OF = re.compile(r'.*\bof\b.*')

			# rels = nltk.sem.extract_rels('PER', 'ORG', 
			# 	nameEnt, corpus='ace', pattern=OF)

			#print(rels)

			for rel in nltk.sem.extract_rels('GPE', 'PER', 
				nameEnt, corpus='ace', pattern=OF):
				print(nltk.sem.rtuple(rel))
			
			#nameEnt.draw()
	except Exception as e:
		print(str(e))

#process_content()

def process_content_relation():
	IN = re.compile(r'.*\bin\b(?!\b.+ing)')
	for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
		for rel in nltk.sem.extract_rels('ORG', 'LOC', doc,
		 corpus='ieer', pattern=IN):
			print(nltk.sem.rtuple(rel))

#process_content_relation()

#tokens = nltk.word_tokenize(raw)

#tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(tagged)

#print(soup.title)

# textTokens = nltk.Text(tokens)
# print(textTokens[100:150])
# print(tokens)