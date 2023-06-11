# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Categorie
from resources.verification import token_required


class EventCatrgorie(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    room_mandatory = Namespace(name='room_mandatory', default=0, dest="room_mandatory", action='store', type=bool)
    prestataire_mandatory = Namespace(name='prestataire_mandatory', default=0, dest="prestataire_mandatory", action='store', type=bool)

 
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
    
    
    @token_required
    def post(self, user):
        """
            Get an Product
            :params:    name: name of the product to create
                        description: description of the product to create
                        stock: stock of the product to create
                        prix: prix of the product to create
                        store_id: store of the product to create

            :return: Product json data. 
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.room_mandatory)))
        parser.add_argument(**vars(self.__required__(self.prestataire_mandatory)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            categorie = Categorie(room_mandatory=data['room_mandatory'], prestataire_mandatory=data['prestataire_mandatory'])
            if not categorie:
                abort(405, 'Categorie could not be found')

            try:
                categorie.add_to_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the categorie')

            categorie_json = categorie.json()
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

        data = parser.parse_args()
        del parser

        if data['id']: 

            categorie = Categorie.find_by_id(id=data['id'])
            if not categorie:
                abort(405, 'Categorie could not be found')

            json_categorie = categorie.json()

        else:
            categorie_list = Categorie.find_all()
            if not categorie_list:
                abort(405, 'Categorie list could not be found')

            json_categorie = Categorie.all_json(categorie_list=categorie_list)

        response = current_app.response_class(response=json.dumps(json_categorie), status=200,
                                                      mimetype='application/json')
        return response


    @token_required
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
            categorie = Categorie.find_by_id(id=data['id'])
            if not categorie:
                abort(405, 'Prestataire could not be found')
                
            categorie.remove_from_db()

        response = current_app.response_class(response=json.dumps({'message':'categorie deleted'}), status=203, mimetype='application/json')

        return response
