# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import Product


class ProductInStore(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    store_id = Namespace(name='store_id', default=0, dest="store_id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
    description = Namespace(name='description', default=0, dest="description", action='store', type=str)
    stock = Namespace(name='stock', default=0, dest="stock", action='store', type=int)
    prix = Namespace(name='prix', default=0, dest="prix", action='store', type=float)
    note = Namespace(name='note', default=0, dest="note", action='store', type=float)

 
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
        parser.add_argument(**vars(self.__required__(self.name)))
        parser.add_argument(**vars(self.__required__(self.description)))
        parser.add_argument(**vars(self.__required__(self.stock)))
        parser.add_argument(**vars(self.__required__(self.prix)))
        parser.add_argument(**vars(self.__required__(self.store_id)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            product = Product(store_id=data['store_id'], name=data['name'], description=data['description'], stock=data['stock'], prix=data['prix'])

            try:
                product.add_to_db()


            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the product')

            store_json = product.json() 
            response = current_app.response_class(response=json.dumps(store_json), status=201,
                                                mimetype='application/json')
            return response


    def get(self):
        """
            Get an Product
            :params:    name: name of the product to get

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
            try:
                product = Product.find_by_name(name=data['name'])
                response = current_app.response_class(response=json.dumps(product.json()), status=200,
                                                      mimetype='application/json')
                return response

            except Exception as e:
                logging.error(e)
                abort(400, 'An error occurred retrieving the product')


    def delete(self):
        """
            Delete a Product
            :params:    name: nameof the product to delete

            :return: str
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
            product = Product.find_by_name(name=data['name'])
            if not product:
                logging.error('USER NOT FOUND')

                abort(405, 'Product could not be found')
            product.remove_from_db()
        response = current_app.response_class(response=json.dumps(dict(message='product deleted')), status=204, mimetype='application/json')

        return response


    def patch(self):
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
        parser.add_argument(**vars(self.__required__(self.name)))
        parser.add_argument(**vars(self.__optional__(self.description)))
        parser.add_argument(**vars(self.__optional__(self.stock)))
        parser.add_argument(**vars(self.__optional__(self.prix)))

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

            product = Product.find_by_name(name=data['name'])

            if not product:
                abort(404, dict(message='Product could not be found'))
            try:
                product.patch_in_db(keys_to_patch)
            except Exception as e:
                logging.error(e) 
                response = current_app.response_class(response=json.dumps(dict(message=keys_to_patch)), status=405, mimetype='application/json')

                abort(405, 'Missing required parameter in the JSON body')
            response = current_app.response_class(response=json.dumps(dict(message='product udpated')), status=204, mimetype='application/json')
            return response