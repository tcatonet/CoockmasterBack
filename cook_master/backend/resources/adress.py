# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import Adress
from resources.verification import token_required


class UserAdress(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    user_id = Namespace(name='user_id', default=0, dest="user_id", action='store', type=int)
    city = Namespace(name='city', default=0, dest="city", action='store', type=str)
    postcode = Namespace(name='postcode', default=0, dest="postcode", action='store', type=str)
    adress = Namespace(name='adress', default=0, dest="adress", action='store', type=str)

 
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
        parser.add_argument(**vars(self.__required__(self.city)))
        parser.add_argument(**vars(self.__required__(self.postcode)))
        parser.add_argument(**vars(self.__required__(self.adress)))

        try:
            data = parser.parse_args()
            del parser
 
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
          
        else: 
            adress = Adress(city=data['city'], postcode=data['postcode'], adress=data['adress'], user_id=user.id)
            if not adress:
                abort(405, 'Adress could not be found')
            try:
                adress.add_to_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the adress')

            adress_json = adress.json()
            response = current_app.response_class(response=json.dumps(adress_json), status=201,
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
                 
            if data['id'] in data: 
                adress = Adress.find_by_id(id=data['id'], user_id=user.id)
                if not adress:
                    abort(405, 'Adress could not be found')

                json_adress = adress.json() 
 
            else:
                adress_list = Adress.find_all(user_id=user.id)
                if not adress_list:
                    abort(405, 'Adress list could not be found')

                json_adress = Adress.all_json(adress_list=adress_list)
 
        response = current_app.response_class(response=json.dumps(json_adress), status=200,
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
            adress = Adress.find_by_id(id=data['id'], user_id=user.id)
            if not adress:
                abort(405, 'Product could not be found')

            adress.remove_from_db()
        response = current_app.response_class(response=json.dumps(dict(message='adress deleted')), status=204, mimetype='application/json')

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
        parser.add_argument(**vars(self.__optional__(self.city)))
        parser.add_argument(**vars(self.__optional__(self.postcode)))
        parser.add_argument(**vars(self.__optional__(self.adress)))

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

            adress = Adress.find_by_id(id=data['id'], user_id=user.id)
            if not adress:
                abort(404, dict(message='Adress could not be found'))
 
            try:
                adress.patch_in_db(keys_to_patch) 
            except Exception as e:
                logging.error(e)  
                response = current_app.response_class(response=json.dumps(dict(message=keys_to_patch)), status=405, mimetype='application/json')

                abort(405, 'Missing required parameter in the JSON body')
            response = current_app.response_class(response=json.dumps(dict(message='adress udpated')), status=204, mimetype='application/json')
            return response 