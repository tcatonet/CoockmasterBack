# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import Product, Avis, Store
from resources.verification import admin_token_required


class ProductInStore(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    store_id = Namespace(name='store_id', default=0, dest="store_id", action='store', type=int)
    product_categorie_id = Namespace(name='product_categorie_id', default=0, dest="product_categorie_id", action='store', type=int)

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
    
    @admin_token_required
    def post(self, user):
        """
            Post a Product
            :params:    name: name of the product to create
                        description: description of the product to create
                        stock: stock of the product to create
                        prix: prix of the product to create
                        store_id: store of the product to create
                        product_categorie_id: product categori of the product to create

            :return: Product json data.    
            :rtype: application/json. 
        """     
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.name)))
        parser.add_argument(**vars(self.__required__(self.description)))
        parser.add_argument(**vars(self.__required__(self.stock)))
        parser.add_argument(**vars(self.__required__(self.prix))) 
        parser.add_argument(**vars(self.__required__(self.store_id)))
        parser.add_argument(**vars(self.__optional__(self.product_categorie_id)))
 
        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
         
        else:
            if data['prix']:
                if data['prix']  < 0:
                    abort(400, 'invalid prix')
            else:
                abort(400, 'invalid prix')

            if data['stock']:
                if data['stock']  < 0:
                    abort(400, 'invalid stock')
            else:
                abort(400, 'invalid prix')

            if data['name']:
                if data['name']  == '':
                    abort(400, 'name cannot be null')
            else:
                abort(400, 'invalid prix')

            store_id = Store.find_by_id(id=data['store_id'])

            if not store_id: 
                abort(400, 'store cannot be null')

            product = Product(store_id=data['store_id'], product_categorie_id=data['product_categorie_id'], name=data['name'], description=data['description'], stock=data['stock'], prix=data['prix'])
            if not product:
                abort(404, 'Product could not be found')

            try:
                product.add_to_db()
                product_json = product.json(product_avis=[]) 

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the product')

            else:
                response = current_app.response_class(response=json.dumps(product_json), status=201,
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
            product = Product.find_by_name(name=data['name'])
            if not product:
                abort(405, 'Product could not be found')

            try:
                avis_list = Avis.find_all_by_product_id(product_id=product.id)
                json_list_avis = Avis.all_json(avis_list)

            except Exception as e:
                logging.error(e)
                abort(400, 'An error occurred retrieving the product') 
                
            else:
                response = current_app.response_class(response=json.dumps(product.json(product_avis=json_list_avis)), status=200,
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
                abort(405, 'Product could not be found')

            try:
                product.remove_from_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the product')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='product deleted')), status=204, mimetype='application/json')
                return response


    @admin_token_required
    def patch(self, user): 
        """
            Patch a Product
            :params:    name: name of the product to patch
                        description: description of the product to patch
                        stock: stock of the product to patch
                        prix: prix of the product to patch

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
            if data['prix']:
                if data['prix']  < 0:
                    abort(400, 'invalid prix')

            if data['stock']:
                if data['stock']  < 0:
                    abort(400, 'invalid stock')

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
                abort(422, 'An error occurred patching the product')

            else:
                response = current_app.response_class(response=json.dumps(dict(message=keys_to_patch)), status=204, mimetype='application/json')
                return response