import requests, json
from collections import Counter
from samples.database import pymysql_connect

# -*- coding: utf-8 -*- 


# Round points function from a list of points (coordenates)
def roundPoints(points):
	pointList = [[round(float(point[0]), 1), round(float(point[1]), 1)] for point in points]
	return pointList

# Return que most frequent point in the list	
def mostFreqPoint(points):
	points_to_count = [point[0] for point in points]
	c = Counter(points_to_count).most_common(1)
	most_freq_point = [point for point in points if c[0][0] == point[0]]
	return most_freq_point

# Funcao que percorre a lista de adjacencia a encontra os
# lugares que casam com o nome passado
# def matchPlacesAdj(places, placeId):


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
apiServiceEntity = "api/place/entity/name/"


# Busca todas as entidades não classificadas como lugar
# que estão relacionadas ao lugar (placeId)
apiServiceLocations = "api/entity/relatedPlace/"

# Nomes e PlaceIds
placeName = "New York"
placeId = ""
entityName = "Obama"

# URLs por serviços
url = baseUrl + apiServiceEntity + entityName
urlNamesByPlaceId = baseUrl + apiServiceNamesByPlaceId + placeId
urlNamesByPlaceName = baseUrl + apiServicePlacesByName + placeName

response = requests.get(urlNamesByPlaceName)

# ************ Fim do acesso ao LOG ***************


# Obtem a resposta string JSON em formato Object
respObject = json.loads(response.text)

print(respObject['results'])

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
