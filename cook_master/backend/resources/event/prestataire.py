# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging
import re

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Prestataire, PrestataireInEvent
from resources.verification import token_required, admin_token_required
from utils.validation import valid_email_regex

from utils.global_config import ADMIN_LEVEL


class CompanyPrestataire(Resource):

    """ Prestataire endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    lastname = Namespace(name='lastname', default=0, dest="lastname", action='store', type=str)
    firstname = Namespace(name='firstname', default=0, dest="firstname", action='store', type=str)
    email = Namespace(name='email', default=0, dest="email", action='store', type=str)
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
    
    
    @admin_token_required
    def post(self, user):
        """
            Get an Prestataire
            :params:    lastname: lastname of the Prestataire to create
                        firstname: firstname of the Prestataire to create
                        activite: activite of the Prestataire to create
                        description: description of the Prestataire to create

            :return: Prestataire json data.  
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.lastname)))
        parser.add_argument(**vars(self.__required__(self.firstname)))
        parser.add_argument(**vars(self.__required__(self.email)))
        parser.add_argument(**vars(self.__required__(self.activite)))
        parser.add_argument(**vars(self.__required__(self.description)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if not re.match(valid_email_regex, data['email']):
                abort(400, 'invalid email')
            if data['firstname'] == '':
                abort(400, 'invalid firstname')
            if data['lastname'] == '':
                abort(400, 'invalid lastname')
            if data['description'] == '':
                abort(400, 'invalid description')
            if data['activite'] == '':
                abort(400, 'invalid activite')

            existing_prestataire= Prestataire.find_by_email(email=data['email'])
            if existing_prestataire:
                abort(400, 'prestataire already exist')

            prestataire = Prestataire(lastname=data['lastname'], firstname=data['firstname'], activite=data['activite'], description=data['description'])

            try:
                prestataire.add_to_db()
                prestataire_json = prestataire.json_admin()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the Prestataire')

            else:
                response = current_app.response_class(response=json.dumps(prestataire_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def get(self, user):
        """
            Get an Prestataire
            :params:    id: id of the Prestataire to get

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

            if user.level == ADMIN_LEVEL:
                json_prestataire = prestataire.json_admin()
            else:
                json_prestataire = prestataire.json()

        else:
            prestataire_list = Prestataire.find_all()
            if not prestataire_list:
                abort(405, 'Prestataire list could not be found')

            json_prestataire = Prestataire.all_json(prestataire_list=prestataire_list)

        response = current_app.response_class(response=json.dumps(json_prestataire), status=200,
                                                      mimetype='application/json')
        return response


    @admin_token_required
    def delete(self, user):
        """
            Delete a prestataire
            :params:    id: id of the prestataire to delete

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
                abort(405, 'Prestataire couldPrestataireInEvent not be found')
 
            prestataire_in_events = PrestataireInEvent.find_by_prestataire_id(prestataire_id=prestataire.id)
            for prestataire_in_event in prestataire_in_events:
                try:
                    prestataire_in_event.remove_from_db()
                except Exception as e:
                    logging.error(e) 
                    abort(400, 'Cannot remove prestataire from event')

            try:
                prestataire.remove_from_db() 

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the prestataire')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='prestataire deleted')), status=204, mimetype='application/json')
                return response


    @admin_token_required
    def patch(self, user):
        """
            Patch a Product
            :params:    lastname: lastname of the product to patch
                        description: description of the product to patch
                        stock: stock of the product to patch
                        prix: prix of the product to patch
                        store_id: store of the product to patch

            :return: Product json data 
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.lastname)))
        parser.add_argument(**vars(self.__optional__(self.email)))
        parser.add_argument(**vars(self.__optional__(self.firstname)))
        parser.add_argument(**vars(self.__optional__(self.activite)))
        parser.add_argument(**vars(self.__optional__(self.description)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e) 
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            if data['email']:
                if not re.match(valid_email_regex, data['email']):
                    abort(400, 'invalid email')

                existing_prestataire= Prestataire.find_by_email(email=data['email'])
                if existing_prestataire:
                    abort(400, 'prestataire already exist')

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
                abort(422, 'An error occurred patching the prestataire')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='prestataire udpated')), status=204, mimetype='application/json')
                return response