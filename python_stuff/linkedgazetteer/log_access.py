'''Warning: use NumPy for improve loop statements'''

'''Obs.: Atraves do serviço urlLocationsByEntity no LoG
observa-se que para cada tripla <s, p, o> em que 's' ou 'p' são dos tipos
(pessoa, local), a maior parte das 
entidades (s ou p) não contém como resposta
o local contido na tripla. 

Isso indica que o gazetteer carece de informações relevantes encontradas 
durante a extração da relacionamentos nos artigos da Wikipedia

Ex.: <Susan Crown, be philanthropist of, Chicago>

Acessando o serviço urlLocationsByEntity com a entidade
Susan Crown como parâmetro, nenhum local é retornado como resposta. O que
indica que esse relacionamento pode ser incorporado na base
de dados como pontencial candidato.


'''

import requests, json, re, unicodedata, pycountry
from collections import Counter
from urllib.parse import unquote
from samples.database import pymysql_connect

# -*- coding: utf-8 -*- 


'''Round points function from a list of points (coordenates)'''
def roundPoints(points):
	pointList = [[round(float(point[0]), 1), round(float(point[1]), 1)] for point in points]
	return pointList

'''Return que most frequent point in the list'''
def mostFreqPoint(points):
	points_to_count = [point[0] for point in points]
	c = Counter(points_to_count).most_common(1)
	most_freq_point = [point for point in points if c[0][0] == point[0]]
	return most_freq_point

'''Return a string without accents'''
def delete_accents(data):
	return unicodedata.normalize('NFKD', data).encode('ASCII', 'ignore').decode('ASCII')

'''Return a string without special chars and accents'''
def formatString(string):
	string = delete_accents(string)
	return ''.join(e for e in string if e.isalnum() or e == " ")

'''Return results from url request in Object format'''
def get_data(url):
	try:
		response = requests.get(url)

		# Obtem a resposta string JSON em formato Object
		respObject = json.loads(response.text)
		results = respObject['results']
	except:
		print("requisicao mal sucedida")
		pass	
	return results

'''Return non-place entity from triple''' 
def getPlaceNomPlaceEntities(triple):
	e = []
	l = []
	if(triple[1] != 'LOCATION'):
		e = triple[2]
		l = triple[4]
	else:
		e = triple[4]
		l = triple[2]
	return l, e

'''Return a string with url encoded format parsed''' 
def parse_url_encode(string):
	return unquote(unquote(string))

'''Return a list of values (columns) from results'''
def get_column_from_result(results):
	return [parse_url_encode(result['dbpediaId']) for result in results if result['dbpediaId'] is not None]

'''Return the element most frequent in the list'''
def most_freq_value(list):
	return Counter(list).most_common()

'''Return all upper case characters from a word'''
def all_uppercase_from_word(word):
	return re.sub('[^A-Z]', '', word)

def all_countries():
	return list(pycountry.countries)

'''Verify if a word is a name abbreviation'''
def is_abbreviation(word):
	return True if word.isupper() else False

'''Return specific country name according your abbreviation name'''
def specific_country(country):
	try:
		a = pycountry.countries.get(alpha_2=country)
		#print('abbreviated')
		return a.name
	except:
		try:
			a = pycountry.countries.get(alpha_3=country)
			#print('abbreviated')
			return a.name
		except:
			#print('non abbreviated')
			return country

'''Verify if a locations list contains a specific location name (abbreviated or not)'''
def containsLocation(locations, l):
	# Too verify if l is a abbriviated name and return the name
	print(l)
	if (is_abbreviation(l)):
		print("Is abbrev")
		l = l.replace(".", "")
		s = specific_country(l)
	else:
		s = l
	s = s.replace(" ", "_")
	print(s)
	return True if (s in locations) else False


def place_from_name(triples, url):
	Lp = []
	for t in triples:
		l, e = getPlaceNomPlaceEntities(t)
		urlTemp = url + formatString(e)
		print(urlTemp)
		La = get_data(urlTemp)
		Lb = get_column_from_result(La)
		if (containsLocation(Lb, l)):
			print("Opa contains")

# Funcao que percorre a lista de adjacencia a encontra os
# lugares que casam com o nome passado


# Parte referente do acesso ao LOG

baseUrl = "http://sandwich.lbd.dcc.ufmg.br:8080/linkedOntoGazetteerWeb/"

# Busca todos os lugares que estao associados ao nome passado
# como parametro e os lugares pertencentes a lista de adjacencia 
# dele
apiServicePlaceAdjacentListByName = "api/place/name/adjacentList/"

# Busca todos os nomes dados um lugar (placeId)
apiServiceNamesByPlaceId = "api/name/place/"

# Busca por todos os lugares que 
# estao associados ao nome informado
apiServicePlacesByName = "api/place/name/"


# Busca todas todos os lugares
# que estao relacionadas a entidade (entityName = placeName)
apiServiceLocation = "api/place/entity/name/"


# Busca todas as entidades nao classificadas como lugar
# que estao relacionadas ao lugar (placeId)
apiServiceEntity = "api/entity/relatedPlace/"

# Nomes e PlaceIds
placeName = "US"
placeId = "72178544"

# 1640

# 463356

# 72178544

# 1640

# 41440

entityName = "Barack Obama"

counter = 0

# Feature Classes
numAdministrativeBoundaryF = 0
numPopulatedPlacesF = 0
numAreaF = 0
numHydroF = 0

# Feature Codes
numFirstAdministrativeDivision = 0
numSecondAdministrativeDivision = 0
numPopulatedPlacesByCode = 0
numSeatOfFirstAdmDivision = 0



# URLs por servicos
url = baseUrl + apiServiceEntity + entityName
urlNamesByPlaceId = baseUrl + apiServiceNamesByPlaceId + placeId
urlNamesByPlaceName = baseUrl + apiServicePlacesByName
urlLocationsByEntity = baseUrl + apiServiceLocation
urlEntitiesByLocation = baseUrl + apiServiceEntity + placeId


# Database access to select triples
data = pymysql_connect.database_connection()

#place_from_name(data, urlLocationsByEntity)

#print(containsLocation(["United_States", "Other"], "UK"))

print(all_uppercase_from_word("United_States"))

#response = requests.get(urlLocationsByEntity)
#response = requests.get(urlNamesByPlaceId)
#response = requests.get(urlNamesByPlaceName)

# ************ Fim do acesso ao LOG ***************


# Obtem a resposta string JSON em formato Object
#respObject = json.loads(response.text)

#print(respObject['results'])

# Obtem uma lista de coordenadas
# points = [result['gnPoint'] for result in respObject['results']]
# pointsFormat = [point[5:].replace("[", "").replace("]", "").split(',') for point in points if not(point is None)]

# roundedPoints = roundPoints(pointsFormat)

# print((roundedPoints))

# print(round(float(pointsFormat[0][0]), 2))

# for place in respObject['results']:
# 	#placeId = str(place['_id'])
# 	print(place['gnPoint'])
# 	urlNamesByPlaceId = urlNamesByPlaceId + placeId
# 	response = requests.get(urlNamesByPlaceId)
# 	respObject = json.loads(response.text)
# 	print(respObject)


#Print response body text
#print (respObject['results'])
