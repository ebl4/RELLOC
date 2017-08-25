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
	#return re.findall(r'<script>(.*?)</script>', text)


raw = ""
url = "https://en.wikipedia.org/wiki/Ouro_Preto"
response = urllib.request.urlopen(url)
html = response.read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())


for parag in soup("p"):
	raw += parag.get_text()

#print(raw)

tokens = nltk.word_tokenize(raw)
#print(tokens)

tagged = nltk.pos_tag(tokens)
#print(tagged)

entities = nltk.chunk.ne_chunk(tagged)
print(entities)

# textTokens = nltk.Text(tokens)
# print(textTokens[100:150])
# print(tokens)