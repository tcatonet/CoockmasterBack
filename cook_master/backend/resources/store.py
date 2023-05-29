# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import Store, Product


class StoreProduct(Resource):

    """ Store' endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
    products = Namespace(name='products', default="", dest="products", action='store', type=str, case_sensitive=False)


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
    
 
    def post(self):
        """
            post a Store
            :params:    name: name of the store to create
            
            :return: Product json data
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
            store = Store(name=data['name'])

            try:
                store.add_to_db()
            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred registering the user')

            store_json = store.json() 
            response = current_app.response_class(response=json.dumps(store_json), status=201,
                                                mimetype='application/json')
            return response


    def get(self):
        """
            Get a Store
            :params:    name: name of the store to get

            :return: Product json data
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.name)))
 
        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')

        else:  
            try:
                store_product = Store.find_by_name(name=data['name'])
                products = Product.find_by_store_id(store_id=store_product.id)

                json_product = store_product.all_json(products=products)
                response = current_app.response_class(response=json.dumps(json_product), status=200,
                                                      mimetype='application/json')

                return response
            except ValueError:
                abort(404, str(ValueError))