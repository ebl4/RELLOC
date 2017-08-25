import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF, FOAF
g = rdflib.Graph()
g.load('http://dbpedia.org/resource/Ouro_Preto')

allTriplas = []

op = URIRef("http://dbpedia.org/resource/Ouro_Preto")

minas = URIRef("http://dbpedia.org/resource/Minas_Gerais")

for s, p, o in g:
		allTriplas += [(s,p,o)]

for tripla in allTriplas:
	print tripla[1]