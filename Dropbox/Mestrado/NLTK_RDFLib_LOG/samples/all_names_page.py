import nltk
from bs4 import BeautifulSoup
import urllib.request
import re

def get_text_from(raw):
	return raw

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

url = "https://pt.wikipedia.org/wiki/Ouro_Preto"
response = urllib.request.urlopen(url)
html = response.read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')


for parag in soup("a"):
	print(parag.get_text())


#tokens = nltk.word_tokenize(raw)

#tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(tagged)

#print(soup.title)

print(raw)

# textTokens = nltk.Text(tokens)
# print(textTokens[100:150])
# print(tokens)