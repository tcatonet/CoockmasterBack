# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import ProductCategorie, Product
from resources.verification import admin_token_required


class StoreProductCategorie(Resource):

    """ Store' endpoint. """

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
            post a Categorie 
            :params:    name: name of the Categorie to create
             
            :return: Categorie json data 
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
            product_categorie = ProductCategorie(name=data['name'])
        
            try:
                product_categorie.add_to_db()
                product_categorie_json = product_categorie.json() 

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the Catrgorie')

            else:
                response = current_app.response_class(response=json.dumps(product_categorie_json), status=201,
                                                    mimetype='application/json')
                return response
  

    def get(self):
        """      
            Get a Categorie
            :params:    id: id of the Categorie to get

            :return: Categorie json data
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
                product_categorie = ProductCategorie.find_by_id(id=data['id'])
                if not product_categorie:
                    abort(404, dict(message='Product categorie could not be found'))
                json_product_categorie = product_categorie.json()

            else:
                products_categories = ProductCategorie.get_all()
                json_product_categorie = ProductCategorie.all_json(products_categories)

            response = current_app.response_class(response=json.dumps(json_product_categorie), status=200,
                                                      mimetype='application/json')
            return response
