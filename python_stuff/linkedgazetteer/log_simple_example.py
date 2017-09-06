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
placeName = "Lebanon Township of O'Hara Township of Penn Hills City"
placeId = ""
entityName = "Obama"

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
# urlNamesByPlaceName = baseUrl + apiServicePlacesByName + placeName


# Database access to select triples
data = pymysql_connect.database_connection()

for row in data:
	if (row[1] == "LOCATION" and not(row[2] is None)):
		placeName = row[2]
	elif (row[3] == "LOCATION"):
		placeName = row[4]

	placeName = placeName.replace("/","_").replace("'","_").replace("\\","_")

	urlNamesByPlaceName = baseUrl + apiServicePlacesByName + placeName

	# print(urlNamesByPlaceName)

	try:
		response = requests.get(urlNamesByPlaceName)

		# Obtem a resposta string JSON em formato Object
		respObject = json.loads(response.text)
		results = respObject['results']

		counter += 1
		print(str(counter) + " " + placeName) 

		for result in results:

			if (result['gnFeatureClass'] == 'A'):
				numAdministrativeBoundaryF += 1
			elif (result['gnFeatureClass'] == 'P'):
				numPopulatedPlacesF += 1
			elif (result['gnFeatureClass'] == 'L'):
				numAreaF += 1
			elif (result['gnFeatureClass'] == 'H'):
				numHydroF += 1


			if (result['gnFeatureCode'] == 'ADM1'):
				numFirstAdministrativeDivision += 1
			elif (result['gnFeatureCode'] == 'ADM2'):
				numSecondAdministrativeDivision += 1
			elif (result['gnFeatureCode'] == 'PPL'):
				numPopulatedPlacesByCode += 1
			elif (result['gnFeatureCode'] == 'PPLA'):
				numSeatOfFirstAdmDivision += 1
	except:
		print("deu erro")
		pass				



print(numAdministrativeBoundaryF)
print(numPopulatedPlacesF)
print(numAreaF)
print(numHydroF)

# Feature Codes
print(numFirstAdministrativeDivision)
print(numSecondAdministrativeDivision)
print(numPopulatedPlacesByCode)
print(numSeatOfFirstAdmDivision)



# response = requests.get(urlNamesByPlaceName)

# ************ Fim do acesso ao LOG ***************


# Obtem a resposta string JSON em formato Object
# respObject = json.loads(response.text)

# print(respObject['results'])

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
