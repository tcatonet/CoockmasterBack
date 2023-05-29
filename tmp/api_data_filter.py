# import sys
# import os
# import re
#
# from utils.messages import ErrorMessages
# from utils.success_payload_formatter import response_failure
# from utils.list_departement import LIST_DEPARTEMENT
#
# emailRegex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# passwordRegex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
#
#
# class APIDataFilter:
#
#     def __init__(self, action):
#         self.errorMessage = {}
#         self.action = action
#
#     def check_data(self, data):
#
#         try:
#             formatValidation = True
#
#             for key in data:
#                 formatValidation = self.findKey(key, data) and formatValidation
#
#             return formatValidation
#
#         except Exception as e:
#             raise Exception(e)
#
#     def response_failure_check_data(self):
#         response = response_failure(message={"field": self.errorMessage})
#         return response
#
#     def findKey(self, key, jsonDto):
#
#         if self.checkIsNull(key, jsonDto[key]):
#
#             switcher = {
#                 "authenticate": {
#                     "useremail": self.checkLen(key, jsonDto[key], 1, 40),
#                     "password": self.checkLen(key, jsonDto[key], 1, 40),
#                 },
#
#                 "user/post": {
#                     "username": self.checkLen(key, jsonDto[key], 1, 40),
#                     "email": self.checkEmailFormat(key, jsonDto[key]),
#                     "password": self.checkPasswordFormatForValidation(key, jsonDto[key]),
#                 },
#
#                 "user/patch": {
#                     "username": self.checkLen(key, jsonDto[key], 1, 40),
#                     "newemail": self.checkEmailFormat(key, jsonDto[key]),
#                 },
#
#                 "user/password/patch": {
#                     "password": self.checkLen(key, jsonDto[key], 1, 40),
#                     "newpassword": self.checkPasswordFormatForValidation(key, jsonDto[key]),
#                 },
#
#                 "project/post": {
#                     "name": self.checkLen(key, jsonDto[key], 1, 30),
#                     "description": self.checkLen(key, jsonDto[key], 1, 500),
#                     "departement": self.checkCodeDepartement(key, jsonDto[key]),
#                     "infrastructure": self.checkInfrastructure(key, jsonDto[key]),
#
#                 },
#                 "project/patch": {
#                     "name": self.checkLen(key, jsonDto[key], 1, 30),
#                     "description": self.checkLen(key, jsonDto[key], 1, 500),
#                 },
#                 "project/delete": {
#                     "name": self.checkLen(key, jsonDto[key], 1, 30),
#                     "newname": self.checkLen(key, jsonDto[key], 1, 30),
#                     "password": self.checkLen(key, jsonDto[key], 1, 40),
#                 },
#
#             }
#
#             action_swicher = switcher.get(self.action, {})
#             if key in self.errorMessage:
#                 self.errorMessage[key] += action_swicher.get(key, "")
#             else:
#                 self.errorMessage[key] = action_swicher.get(key, "")
#
#         else:
#             self.errorMessage[key] = " mustn't be null"
#
#         return self.errorMessage[key] == ""
#
#     @staticmethod
#     def checkIsNull(data):
#         result = data != None and data != ""
#         return result
#
#     def checkLen(self, key, data, lenMin, lenMax):
#         resultMax = len(data) <= lenMax
#
#         if not resultMax:
#
#             if key in self.errorMessage:
#                 return " and " + data + " cannot exceed " + str(lenMax) + " characters. Actually " + str(
#                     len(data)) + " characters"
#             else:
#                 return data + " cannot exceed " + str(lenMax) + " characters. Actually " + str(
#                     len(data)) + " characters"
#
#         resultMin = len(data) >= lenMin
#
#         if not resultMin:
#
#             if key in self.errorMessage:
#                 return " and " + data + " must be composed of at least " + str(lenMax) + "; actually " + str(
#                     len(data)) + " characters"
#             else:
#                 return data + " must be composed of at least " + str(lenMax) + "; actually " + str(
#                     len(data)) + " characters"
#
#         return ""
#
#     def checkEmailFormat(self, key, data):
#         result = re.search(emailRegex, data)
#
#         if not result:
#
#             if key in self.errorMessage:
#                 return " and " + ErrorMessages.WRONG_EMAIL_CHECK_ERROR
#             else:
#                 return ErrorMessages.WRONG_EMAIL_CHECK_ERROR
#
#         return ""
#
#     def checkPasswordFormat(self, key, data):
#         result = re.search(passwordRegex, data)
#
#         if not result:
#
#             if key in self.errorMessage:
#                 return " and " + ErrorMessages.FORMAT_PASSWORD_CHECK_ERROR
#             else:
#                 return ErrorMessages.FORMAT_PASSWORD_CHECK_ERROR
#
#         return ""
#
#     def checkPasswordFormatForValidation(self, key, data):
#         result = re.search(passwordRegex, data)
#
#         if not result:
#
#             if key in self.errorMessage:
#                 return " and " + ErrorMessages.FORMAT_PASSWORD_CHECK_ERROR
#             else:
#                 return ErrorMessages.FORMAT_PASSWORD_CHECK_ERROR
#
#         return ""
#
#     def checkPasswordEqualPassword2(self, newUserPassword2, jsonDto, key):
#
#         if "newUserPassword" in jsonDto:
#             result = jsonDto["newUserPassword"] == newUserPassword2
#         else:
#             result = False
#
#         if not result:
#
#             if "newUserPassword2" in self.errorMessage:
#                 return " and " + ErrorMessages.SAME_ACCOUNT_PASSWORD_CHECK_ERROR
#             else:
#                 return ErrorMessages.SAME_ACCOUNT_PASSWORD_CHECK_ERROR
#
#         return ""
#
#     def checkInfrastructure(self, key, data):
#         result = data in ["habitation", "autoroute"]
#
#         if not result:
#
#             if key in self.errorMessage:
#                 return " and " + ErrorMessages.WRONG_INFRA_CHECK_ERROR
#             else:
#                 return ErrorMessages.WRONG_INFRA_CHECK_ERROR
#
#         return ""
#
#     def checkCodeDepartement(self, key, data):
#         result = data in LIST_DEPARTEMENT
#
#         if not result:
#             if key in self.errorMessage:
#                 return " and " + ErrorMessages.WRONG_INSEE_CHECK_ERROR
#             else:
#                 return ErrorMessages.WRONG_INSEE_CHECK_ERROR
#
#         return ""
