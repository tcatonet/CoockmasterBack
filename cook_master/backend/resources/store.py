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
    page = Namespace(name='page', default=0, dest="page", action='store', type=int)
    min_price = Namespace(name='min_price', default=0, dest="min_price", action='store', type=int)
    max_price = Namespace(name='max_price', default=0, dest="max_price", action='store', type=int)
    product_categorie_id = Namespace(name='product_categorie_id', default=0, dest="product_categorie_id", action='store', type=int)
    note_min = Namespace(name='note_min', default=0, dest="note_min", action='store', type=int)

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
                store_json = store.json() 

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred registering the user')

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
        parser.add_argument(**vars(self.__required__(self.name)))
        parser.add_argument(**vars(self.__required__(self.page)))
        parser.add_argument(**vars(self.__optional__(self.min_price)))
        parser.add_argument(**vars(self.__optional__(self.max_price)))
        parser.add_argument(**vars(self.__optional__(self.product_categorie_id)))
        parser.add_argument(**vars(self.__optional__(self.note_min)))

        try: 
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')

        else:  
            if data['page']:
                if data['page'] < 1:
                    abort(400, 'Wrong page number')

            if data['min_price']:
                if data['min_price'] < 0:
                    abort(400, 'Wrong price')
 
            if data['max_price']:
                if data['max_price'] < 0:
                    abort(400,'Wrong price')

            if data['max_price'] and data['min_price']: 
                if data['max_price'] < data['min_price']:
                    abort(400, 'Wrong price')


            if data['note_min']:
                if data['note_min'] >= 0 and data['note_min'] <= 10:
                    abort(400,'Wrong note')


            try:
                store_product = Store.find_by_name(name=data['name'])
                if not store_product:
                    abort(404, dict(message='Store product could not be found'))

                products = Product.find_by_store_id(store_id=store_product.id)
                if not products:
                    abort(404, dict(message='Products could not be found'))


                json_product = store_product.all_json(products=products)
                response = current_app.response_class(response=json.dumps(json_product), status=200,
                                                      mimetype='application/json')

                return response
            except ValueError:
                abort(404, 'An error occured in get product')