# # BRAIZET Rémi
# # Version 1.0
#
# import sys
# import os
# import requests
# import json
# from PIL import ImageColor
# import logging
# from flask_restful import reqparse
# import tempfile
#
# from models.geodata import GeoDataModel
#
#
# class LoadGeoData:
#     """GeoData' endpoint."""
#
#     def load_georisk_data(self, departement):
#         """
#           get one project for one user.
#           params: userid int
#                   user password str
#           :return: success or failure.
#           :rtype: application/json response.
#         """
#
#         geo_data = GeoDataModel.find_by_departement(departement=departement)
#
#         listCommuneRq = ""
#         listRq = []
#         cpt = 0
#         communeSpec = {}
#
#         for commune_data in geo_data:
#             commune = commune_data.datageojson
#             codeInsee = commune["properties"]["codgeo"]
#             GeoDataModel.find_by_departement(departement=departement)
#
#             if not commune_data.geodataload:
#
#                 # On crée des string de 10 codes communes car georisk ne peut pas traiter plus de 10 commune à la fois
#                 if cpt > 9:
#                     cpt = 0
#                     listRq.append(listCommuneRq)
#                     listCommuneRq = ""
#
#                 if listCommuneRq == "":
#                     listCommuneRq = codeInsee
#
#                 else:
#                     listCommuneRq = listCommuneRq + "," + codeInsee
#
#                 cpt += 1
#
#         if listCommuneRq != '':
#             listRq.append(listCommuneRq)
#
#         cpt = 0
#
#         for listCommune in listRq:
#             geo_risk_ws_earthquake = GeoRiskWSEarthquake(listCommune)
#             geo_risk_ws_radon = GeoRiskWSRadon(listCommune)
#             geo_risk_ws_flood = GeoRiskWSFlood(listCommune)
#
#             print(cpt)
#             cpt += 1
#
#             for commune in geo_risk_ws_earthquake.response_request:
#                 codeInsee = commune["code_insee"]
#                 payload = {
#                     "earthquakeValue": commune["zone_sismicite"],
#                     "earthquakeColor": getEartquakeColor(commune["zone_sismicite"][0])
#                 }
#
#                 communeSpec[codeInsee] = {
#                     **payload
#                 }
#
#             for commune in geo_risk_ws_radon.response_request:
#                 codeInsee = commune["code_insee"]
#                 payload = {
#                     "radonValue": commune["classe_potentiel"],
#                     "radonColor": getRadonColor(commune["classe_potentiel"][0])
#                 }
#
#                 communeSpec[codeInsee] = {
#                     **communeSpec[codeInsee],
#                     **payload
#                 }
#
#             for commune in geo_risk_ws_flood.response_request:
#                 codeInsee = commune["code_insee"]
#                 geo_risk_ws_flood.list_commune_res.append(codeInsee)
#                 payload = {
#                     "floodValue": "Zone innondable",
#                     "floodColor": getFloodColor("2")
#                 }
#
#                 communeSpec[codeInsee] = {
#                     **communeSpec[codeInsee],
#                     **payload
#                 }
#
#             for code_commune in listCommune.split(','):
#                 if code_commune not in geo_risk_ws_flood.list_commune_res:
#                     payload = {
#                         "floodValue": "Zone sûr",
#                         "floodColor": getFloodColor("1")
#                     }
#
#                     communeSpec[code_commune] = {
#                         **communeSpec[code_commune],
#                         **payload
#                     }
#
#             for code_commune in listCommune.split(','):
#                 communeSpec[code_commune]["generalColor"] = getMoyenneColor(
#                     [communeSpec[code_commune]["earthquakeColor"], communeSpec[code_commune]["radonColor"],
#                      communeSpec[code_commune]["floodColor"]])
#
#         res = []
#
#         for commune_data in geo_data:
#
#             commune = commune_data.datageojson
#
#             codeInsee = commune["properties"]["codgeo"]
#             departement = commune["properties"]["dep"]
#
#             geoDataForOneCommune = {}
#
#             if codeInsee in communeSpec:
#                 geoDataForOneCommune = communeSpec[codeInsee]
#
#             commune["properties"] = {
#                 **commune["properties"],
#                 **geoDataForOneCommune
#             }
#             geo_data_model = GeoDataModel(departement=departement, codecommune=codeInsee, datageojson=commune)
#             GeoDataModel.update_geo_data(geo_data_model=geo_data_model, codecommune=codeInsee)
#
#     def geo_data_load_and_save(self):
#
#         if GeoDataModel.is_empty():
#             logging.warning('Goedata Loading')
#             logging.warning('Loading ...')
#
#             geoData = self.get_geo_data_request()
#
#             for communeData in geoData["features"]:
#                 departement = communeData["properties"]["dep"]
#                 code_commune = communeData["properties"]["codgeo"]
#                 geo_data = GeoDataModel(departement=departement, codecommune=code_commune, datageojson=communeData)
#                 geo_data.save_to_db()
#
#             logging.warning('Loading End ')
#
#     def get_geo_data_request(self):
#
#         URL = 'https://www.data.gouv.fr/fr/datasets/r/fb3580f6-e875-408d-809a-ad22fc418581'
#         file = requests.get(URL, stream=True)
#
#         tempfilename = "%s/geodata_file_temp.json" % (tempfile.gettempdir())
#
#         with open(tempfilename, "wb") as json_data:
#             for chunk in file.iter_content(chunk_size=1024):
#
#                 if chunk:
#                     json_data.write(chunk)
#
#         with open(tempfilename) as json_data:
#             data_dict = json.load(json_data)
#             return data_dict
#
#
# def getEartquakeColor(value):
#     getColor = {
#         "1": "#F0F8FF",
#         "2": "#FAEBD7",
#         "3": "#FFA500",
#         "4": "#FF4500",
#         "5": "#FF0000"
#     }
#     return getColor[str(value)]
#
#
# def getRadonColor(value):
#     getColor = {
#         "1": "#F0F8FF",
#         "2": "#FFA500",
#         "3": "#FF0000"
#     }
#     return getColor[str(value)]
#
#
# def getFloodColor(value):
#     getColor = {
#         "1": "#F0F8FF",
#         "2": "#FF0000"
#     }
#     return getColor[str(value)]
#
#
# def getMoyenneColor(inputDataList):
#     sumRgb = (0, 0, 0)
#     for spec in inputDataList:
#         rgbColor = ImageColor.getcolor(spec, "RGB")
#         sumRgb = (rgbColor[0], rgbColor[1], rgbColor[2])
#
#     moyenneHexaColor = '#{:02x}{:02x}{:02x}'.format(int(sumRgb[0] / len(inputDataList)),
#                                                     int(sumRgb[1] / len(inputDataList)),
#                                                     int(sumRgb[2] / len(inputDataList)))
#     return moyenneHexaColor
#
#
# class GeoRiskWSEarthquake():
#
#     def __init__(self, list_code_commune):
#         self.url = "https://www.georisques.gouv.fr/api/v1/zonage_sismique"
#         self.data_url = self.generate_data_url(list_code_commune)
#         self.response_request = self.get_request()
#
#     def get_request(self) -> json:
#         headers = {"Content-Type": "application/json; charset=utf-8"}
#         response = requests.get(self.url + self.data_url, headers=headers)
#         return response.json()['data']
#
#     def generate_data_url(self, list_code_commune) -> str:
#         return "?code_insee=" + list_code_commune
#
#
# class GeoRiskWSFlood():
#
#     def __init__(self, list_code_commune):
#         self.url = "https://www.georisques.gouv.fr/api/v1/gaspar/tri"
#         self.data_url = self.generate_data_url(list_code_commune)
#         self.response_request = self.get_request()
#         self.list_commune_res = []
#
#     def get_request(self) -> json:
#         headers = {"Content-Type": "application/json; charset=utf-8"}
#         response = requests.get(self.url + self.data_url, headers=headers)
#         return response.json()['data']
#
#     def generate_data_url(self, list_code_commune) -> str:
#         return "?code_insee=" + list_code_commune
#
#
# class GeoRiskWSRadon():
#
#     def __init__(self, list_code_commune):
#         self.url = "https://www.georisques.gouv.fr/api/v1/radon"
#         self.data_url = self.generate_data_url(list_code_commune)
#         self.response_request = self.get_request()
#
#     def get_request(self) -> json:
#         headers = {"Content-Type": "application/json; charset=utf-8"}
#         response = requests.get(self.url + self.data_url, headers=headers)
#         return response.json()['data']
#
#     def generate_data_url(self, list_code_commune) -> str:
#         return "?code_insee=" + list_code_commune
