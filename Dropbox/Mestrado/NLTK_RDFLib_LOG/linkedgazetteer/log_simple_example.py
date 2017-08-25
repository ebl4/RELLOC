import requests, json
from collections import Counter


# Round points function from a list of points (coordenates)
def roundPoints(points):
	pointList = [[round(float(point[0]), 1), round(float(point[1]), 1)] for point in points]
	return pointList

# Return que most frequent point in the list	
def mostFreqPoint(points):
	points_to_count = [point[0] for point in points]
	c = Counter(points_to_count)
	print(c.most_common(1))


# Parte referente do acesso ao LOG

baseUrl = "http://sandwich.lbd.dcc.ufmg.br:8080/linkedOntoGazetteerWeb/"

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


placeName = "New York"
placeId = ""
entityName = "Obama"


url = baseUrl + apiServiceEntity + entityName
urlNamesByPlaceId = baseUrl + apiServicePlacesByName + placeName

response = requests.get(urlNamesByPlaceId)

# ************ Fim do acesso ao LOG ***************


# Obtem a resposta string JSON em formato Object
respObject = json.loads(response.text)

# Obtem uma lista de coordenadas
points = [result['gnPoint'] for result in respObject['results']]
pointsFormat = [point[5:].replace("[", "").replace("]", "").split(',') for point in points if not(point is None)]

roundedPoints = roundPoints(pointsFormat)

mostFreqPoint(roundedPoints)

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
