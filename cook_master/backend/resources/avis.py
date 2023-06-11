# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import Avis, Product
from resources.verification import token_required


class UserAvis(Resource):

    """ Product endpoint. """
 
    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    product_in_order_id = Namespace(name='product_in_order_id', default=0, dest="product_in_order_id", action='store', type=int)
    product_id = Namespace(name='product_id', default=0, dest="product_id", action='store', type=int)
    comentary = Namespace(name='comentary', default=0, dest="comentary", action='store', type=str)
    note = Namespace(name='note', default=0, dest="note", action='store', type=int)

 
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
        parser.add_argument(**vars(self.__required__(self.product_in_order_id)))
        parser.add_argument(**vars(self.__required__(self.product_id)))
        parser.add_argument(**vars(self.__required__(self.comentary)))
        parser.add_argument(**vars(self.__required__(self.note)))
        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:

            if data['note'] > 10 or data['note'] < 0:
                abort(400, 'Rate out of range')

            avis = Avis.find_by_order_and_product(product_in_order_id=data['product_in_order_id'], product_id=data['product_id'])
            if avis:
                abort(400, 'You cannot create more than one comentary for one product order')

            avis = Avis(
                product_in_order_id=data['product_in_order_id'],
                product_id=data['product_id'],
                comentary=data['comentary'],
                note=data['note'],
                username=user.username)

            if not avis:
                abort(405, 'Avis could not be found')

            try:

                product = Product.find_by_id(_id=data['product_id'])
                avis_list = Avis.find_all_by_product_id(product_id=product.id)
                keys_to_patch = dict()

                i=0
                if avis_list:
                    
                    for a in avis_list:
                        i+=1
                
                current_note = product.note if product.note else 0
                keys_to_patch['note'] = round(((current_note*i)+data['note']) / (i+1), 2)

                avis.add_to_db()
                product.patch_in_db(keys_to_patch)

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the avis')

            avis_json = avis.json(user_name=user.username)
            response = current_app.response_class(response=json.dumps(avis_json), status=201,
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
            avis = Avis.find_by_id(id=data['id'], user_id=data['user_id'])
            if not avis:
                abort(405, 'Prestataire could not be found')
                
            avis.remove_from_db()

        response = current_app.response_class(response=json.dumps({'message':'avis deleted'}), status=203, mimetype='application/json')

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
        parser.add_argument(**vars(self.__optional__(self.comentary)))
        parser.add_argument(**vars(self.__optional__(self.note)))

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
        
            avis = Avis.find_by_id(id=data['id'], user_id=data['user_id'])
            if not avis:
                abort(404, dict(message='Prestataire could not be found'))

            try:
                avis.patch_in_db(keys_to_patch)
                
            except Exception as e:
                logging.error(e) 
                response = current_app.response_class(response=json.dumps(dict(message=keys_to_patch)), status=405, mimetype='application/json')

                abort(405, 'Missing required parameter in the JSON body')
            response = current_app.response_class(response=json.dumps(dict(message='avis udpated')), status=204, mimetype='application/json')
            return response