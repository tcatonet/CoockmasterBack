# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Prestataire
from resources.verification import token_required


class CompanyPrestataire(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    nom = Namespace(name='nom', default=0, dest="nom", action='store', type=str)
    prenom = Namespace(name='prenom', default=0, dest="prenom", action='store', type=str)
    activite = Namespace(name='activite', default=0, dest="activite", action='store', type=str)
    description = Namespace(name='description', default=0, dest="description", action='store', type=str)

 
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
        parser.add_argument(**vars(self.__required__(self.nom)))
        parser.add_argument(**vars(self.__required__(self.prenom)))
        parser.add_argument(**vars(self.__required__(self.activite)))
        parser.add_argument(**vars(self.__required__(self.description)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            prestataire = Prestataire(nom=data['nom'], prenom=data['prenom'], activite=data['activite'], description=data['description'])
            if not prestataire:
                abort(405, 'Prestataire could not be found')

            try:
                prestataire.add_to_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the room')

            prestataire_json = prestataire.json()
            response = current_app.response_class(response=json.dumps(prestataire_json), status=201,
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

            prestataire = Prestataire.find_by_id(id=data['id'])
            if not prestataire:
                abort(405, 'Prestataire could not be found')

            json_prestataire = prestataire.json()

        else:
            prestataire_list = Prestataire.find_all()
            if not prestataire_list:
                abort(405, 'Prestataire list could not be found')

            json_prestataire = Prestataire.all_json(prestataire_list=prestataire_list)

        response = current_app.response_class(response=json.dumps(json_prestataire), status=200,
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
            prestataire = Prestataire.find_by_id(id=data['id'])
            if not prestataire:
                abort(405, 'Prestataire could not be found')

            if not prestataire:
                logging.error('ADRESS NOT FOUND')

                abort(405, 'Product could not be found')
            prestataire.remove_from_db()
        response = current_app.response_class(response=json.dumps(dict(message='prestataire deleted')), status=204, mimetype='application/json')

        return response


    @token_required
    def patch(self, user):
        """
            Patch a Product
            :params:    name: name of the product to patch
                        description: description of the product to patch
                        stock: stock of the product to patch
                        prix: prix of the product to patch
                        store_id: store of the product to patch

            :return: Product json data 
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.nom)))
        parser.add_argument(**vars(self.__optional__(self.prenom)))
        parser.add_argument(**vars(self.__optional__(self.activite)))
        parser.add_argument(**vars(self.__optional__(self.description)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e) 
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '': 
                    keys_to_patch[key] = data[key]
        
            prestataire = Prestataire.find_by_id(id=data['id'])
            if not prestataire:
                abort(404, dict(message='Prestataire could not be found'))

            try:
                prestataire.patch_in_db(keys_to_patch)
                
            except Exception as e:
                logging.error(e) 
                response = current_app.response_class(response=json.dumps(dict(message=keys_to_patch)), status=405, mimetype='application/json')

                abort(405, 'Missing required parameter in the JSON body')
            response = current_app.response_class(response=json.dumps(dict(message='prestataire udpated')), status=204, mimetype='application/json')
            return response