# # BRAIZET Rémi
# # Version 1.0
#
# import json
# from flask import jsonify
# from flask_restful import Resource, reqparse
# from views.authenticate import token_required, get_token_required
# from flask import Flask, jsonify, request
#
# from models.project import ProjectModel
# from models.user import UserModel
# from utils.messages import ErrorMessages, InfoMessages
# from utils.success_payload_formatter import response_success, response_failure
# from views.api_data_filter import APIDataFilter
# from models.geodata import GeoDataModel
# from views.geodata import LoadGeoData
#
#
# class Project(Resource):
# 	"""Project' endpoint."""
#
# 	parser_create_project = reqparse.RequestParser()
# 	parser_create_project.add_argument(
# 		'name',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_create_project.add_argument(
# 		'description',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_create_project.add_argument(
# 		'infrastructure',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_create_project.add_argument(
# 		'departement',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
#
# 	parser_get_project = reqparse.RequestParser()
# 	parser_get_project.add_argument(
# 		'name',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
#
# 	parser_update_project = reqparse.RequestParser()
# 	parser_update_project.add_argument(
# 		'name',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_update_project.add_argument(
# 		'newname',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_update_project.add_argument(
# 		'description',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
#
# 	parser_delete_project = reqparse.RequestParser()
# 	parser_delete_project.add_argument(
# 		'name',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
# 	parser_delete_project.add_argument(
# 		'password',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
#
# 	@staticmethod
# 	def list_all():
# 		data = ProjectModel.get_all_project()
# 		all_project = []
# 		for d in data:
# 			cur_project = d.__dict__.copy()
# 			del cur_project['_sa_instance_state']
# 			all_project.append(cur_project)
#
# 		return all_project
#
# 	def post(self):
# 		"""
# 		Creates a new project using the provided userid, name, description, departement and infrastructure.
#
# 		:return: success or failure.
# 		:rtype: application/json response.
# 		"""
# 		auth_data = token_required(request)
#
# 		if not auth_data['auth_success']:
# 			return auth_data['message']
#
# 		current_email = auth_data["current_email"]
# 		current_password = auth_data["current_password"]
# 		refresh_token = auth_data["refresh_token"]
#
# 		api_data_filter_auth = APIDataFilter("project/post")
# 		data = Project.parser_create_project.parse_args()
# 		response = None
# 		userid = UserModel.get_id(current_email, current_password)
#
# 		if api_data_filter_auth.check_data(data):
# 			if ProjectModel.find_by_name(userid, data['name']):
# 				response = response_failure(
# 					message="A project with name '{}' for the user {} already exists.".format(data['name'], current_email))
#
# 			else:
# 				data["userid"] = userid
# 				project = ProjectModel(**data)
# 				project.save_to_db()
#
# 				response = response_success(message="Project created successfully.", refresh_token=refresh_token)
# 		else:
# 			response = api_data_filter_auth.response_failure_check_data()
#
# 		return response
#
# 	def get(self):
# 		"""
# 		get one project for one user.
# 		params: userid int
# 						user password str
# 		:return: success or failure.
# 		:rtype: application/json response.
# 		"""
# 		auth_data = get_token_required(request)
#
# 		if not auth_data['auth_success']:
# 			return auth_data['message']
#
# 		current_email = auth_data["current_email"]
# 		current_password = auth_data["current_password"]
# 		refresh_token = auth_data["refresh_token"]
# 		project_name = auth_data["project_name"]
#
# 		loadGeoData = LoadGeoData()
# 		response = None
#
# 		userid = UserModel.get_id(current_email, current_password)
#
# 		if not userid:
# 			response = response_failure(message="The user '{}' does not exist.".format(current_email))
#
# 		project = ProjectModel.find_by_name(userid, project_name)
#
# 		if project:
# 			loadGeoData.load_georisk_data(departement=project.departement)
# 			geo_data = GeoDataModel.find_by_departement(project.departement)
#
# 			json_data = []
#
# 			for data_commune in geo_data:
# 				data_commune = data_commune.__dict__.copy()
# 				del data_commune['_sa_instance_state']
# 				json_data.append(data_commune)
#
# 			response_json_data = {"type": "FeatureCollection", "features": json_data}
# 			#   response = response_success(message="Project retrieve successfully.", refresh_token=refresh_token, data=response_json_data)
# 			response = jsonify(type="FeatureCollection", features=json_data)
#
# 		else:
# 			response = response_failure(message="The project '{}' does not exist.".format(project_name))
#
# 		return response
#
# 	def patch(self):
# 		"""
# 		update one project.
# 		params: userid int
# 						name str
# 		:return: success or failure.
# 		:rtype: application/json response.
# 		"""
# 		auth_data = token_required(request)
#
# 		if not auth_data['auth_success']:
# 			return auth_data['message']
#
# 		current_email = auth_data["current_email"]
# 		current_password = auth_data["current_password"]
# 		refresh_token = auth_data["refresh_token"]
#
# 		api_data_filter_auth = APIDataFilter("project/patch")
# 		data = Project.parser_update_project.parse_args()
# 		userid = UserModel.get_id(current_email, current_password)
#
# 		if api_data_filter_auth.check_data(data):
#
# 			if not userid:
# 				return response_failure(message="The user '{}' does not exist.".format(current_email))
#
# 			project = ProjectModel.find_by_name(userid, data['name'])
# 			newproject = ProjectModel.find_by_name(userid, data['newname'])
#
# 			response = None
#
# 			if project:
# 				if not newproject or data['newname'] == data['name']:
# 					project.update_one_project(userid, data['name'], data['newname'], data["description"])
# 					response = response_success(message="Project update successfully.", refresh_token=refresh_token)
#
#
# 				else:
# 					response = response_failure(message="The project '{}' already exist.".format(data['newname']))
#
# 			else:
# 				response = response_failure(message="The project '{}' does not exist.".format(data['name']))
# 		else:
# 			response = api_data_filter_auth.response_failure_check_data()
#
# 		return response
#
# 	def delete(self):
# 		"""
# 		Finds a project by its username and deletes it.
#
# 		:param username: the username of the user.
# 					 projectname: the projectname of the user.
# 		:type username: str
# 					projectname: str
# 		:return: success or failure.
# 		:rtype: application/json response.
# 		"""
# 		auth_data = token_required(request)
#
# 		if not auth_data['auth_success']:
# 			return auth_data['message']
#
# 		current_email = auth_data["current_email"]
# 		current_password = auth_data["current_password"]
# 		refresh_token = auth_data["refresh_token"]
#
# 		api_data_filter_auth = APIDataFilter("project/delete")
# 		data = Project.parser_delete_project.parse_args()
#
# 		response = None
# 		userid = UserModel.get_id(current_email, current_password)
#
# 		if data['password'] != current_password:
# 			return response_failure(message={"global": "Invalid password"})
#
# 		if api_data_filter_auth.check_data(data):
#
# 			if not userid:
# 				response = response_failure(message="The user '{}' does not exist.".format(current_email))
#
# 			project = ProjectModel.find_by_name(userid, data['name'])
#
# 			if project:
# 				project.delete_from_db()
# 				response = response_success(message='Project deleted', refresh_token=refresh_token)
# 			else:
# 				response = response_failure(message="The project '{}' does not exist.".format(data['name']))
#
# 		else:
# 			response = api_data_filter_auth.response_failure_check_data()
#
# 		return response
#
#
# class Projects(Resource):
# 	"""Project' endpoint."""
#
# 	parser = reqparse.RequestParser()
# 	parser.add_argument(
# 		'name',
# 		type=str,
# 		required=True,
# 		help="This field cannot be left blank!")
#
# 	parser.add_argument(
# 		'password',
# 		type=str,
# 		required=False,
# 		help="This field cannot be left blank!"
# 	)
#
# 	@staticmethod
# 	def list_all():
# 		data = ProjectModel.get_all_project()
# 		all_project = []
# 		for d in data:
# 			cur_project = d.__dict__.copy()
# 			del cur_project['_sa_instance_state']
# 			all_project.append(cur_project)
#
# 		return all_project
#
# 	def get(self):
# 		"""
# 		get all project for one user.
# 		params: userid int
# 						user password str
# 		:return: success or failure.
# 		:rtype: application/json response.
# 		"""
#
# 		auth_data = token_required(request)
#
# 		if not auth_data['auth_success']:
# 			return auth_data['message']
#
# 		current_email = auth_data["current_email"]
# 		current_password = auth_data["current_password"]
# 		refresh_token = auth_data["refresh_token"]
#
# 		userid = UserModel.get_id(current_email, current_password)
# 		data = ProjectModel.find_by_userid(userid)
#
# 		response = None
#
# 		if not userid:
# 			response = response_failure(message="The user '{}' does not exist.".format(current_email))
#
# 		else:
# 			all_project = []
# 			for d in data:
# 				cur_project = d.__dict__.copy()
# 				del cur_project['_sa_instance_state']
# 				all_project.append(cur_project)
#
# 			response = response_success(message="Project list successfully retrieve.", data=all_project,
# 			                            refresh_token=refresh_token)
#
# 		return response