# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.content import CategorieContent
from resources.verification import token_required, admin_token_required


class ContentCatrgorie(Resource): 

    """ Product endpoint. """  
  
    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)

  
    @staticmethod 
    def __required__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = True
        return local_args_namespace

 
    @staticmethod
    def __optional__(arg_namespace):
        local_args_namespace = copy.deepcopy(arg_namespace)
        edit = vars(local_args_namespace)
        edit['required'] = False
        return local_args_namespace
    
    
    @admin_token_required
    def post(self, user):
        """
            Get an event categorie
            :params:    room_mandatory: room_mandatory of the event categorie to create
                        prestataire_mandatory: prestataire_mandatory of the event categorie to create

            :return: Product json data. 
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.name)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if data['name'] == '':
                abort(400, 'invalid name')

            categorie = CategorieContent(name=data['name'])

            try:
                categorie.add_to_db()
                categorie_json = categorie.json()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the event categorie')
                
            else:
                response = current_app.response_class(response=json.dumps(categorie_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def get(self, user):
        """
            Get an Product
            :params:    name: name of the product to get

            :return: Product json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.id)))

        try:
            data = parser.parse_args()
            del parser
        
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if data['id']: 

                categorie = CategorieContent.find_by_id(id=data['id'])
                if not categorie:
                    abort(405, 'Categorie could not be found')

                json_categorie = categorie.json()

            else:
                categorie_list = CategorieContent.find_all()
                if not categorie_list:
                    abort(405, 'Categorie list could not be found')

                json_categorie = CategorieContent.all_json(categorie_list=categorie_list)

            response = current_app.response_class(response=json.dumps(json_categorie), status=200,
                                                        mimetype='application/json')
            return response


    @admin_token_required
    def delete(self, user):
        """
            Delete a Product
            :params:    name: nameof the product to delete

            :return: str
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')

        else:
            categorie = CategorieContent.find_by_id(id=data['id'])
            if not categorie:
                abort(405, 'Categorie could not be found')

            try: 
                categorie.remove_from_db()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred deteting the event categorie')

            else:
                response = current_app.response_class(response=json.dumps({'message':'categorie deleted'}), status=203, mimetype='application/json')
                return response
