'''Warning: use NumPy for improve loop statements'''


import requests, json, re, unicodedata
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

def parse_url_encode(string):
	return unquote(unquote(string))

def get_column_from_result(results):
	return [parse_url_encode(result['dbpediaId']) for result in results if result['dbpediaId'] is not None]

def place_from_name(triples, url):
	Lp = []
	for t in triples:
		l, e = getPlaceNomPlaceEntities(t)
		urlTemp = url + formatString(l)
		print(urlTemp)
		La = get_data(urlTemp)

		print (get_column_from_result(La))

# Funcao que percorre a lista de adjacencia a encontra os
# lugares que casam com o nome passado


# Parte referente do acesso ao LOG

baseUrl = "http://sandwich.lbd.dcc.ufmg.br:8080/linkedOntoGazetteerWeb/"

# Busca todos os lugares que estao associados ao nome passado
# como parametro e os lugares pertencentes à lista de adjacência 
# dele
apiServicePlaceAdjacentListByName = "api/place/name/adjacentList/"

# Busca todos os nomes dados um lugar (placeId)
apiServiceNamesByPlaceId = "api/name/place/"

# Busca por todos os lugares que 
# estão associados ao nome informado
apiServicePlacesByName = "api/place/name/"


# Busca todas todos os lugares
# que estão relacionadas à entidade (entityName = placeName)
apiServiceLocation = "api/place/entity/name/"


# Busca todas as entidades não classificadas como lugar
# que estão relacionadas ao lugar (placeId)
apiServiceEntity = "api/entity/relatedPlace/"

# Nomes e PlaceIds
placeName = "US"
placeId = "9682956"
entityName = "Edward h"

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



# URLs por serviços
url = baseUrl + apiServiceEntity + entityName
urlNamesByPlaceId = baseUrl + apiServiceNamesByPlaceId + placeId
urlNamesByPlaceName = baseUrl + apiServicePlacesByName
urlLocationsByEntity = baseUrl + apiServiceLocation + entityName
urlEntitiesByLocation = baseUrl + apiServiceEntity + placeId


# Database access to select triples
data = pymysql_connect.database_connection()

place_from_name(data, urlNamesByPlaceName)


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
