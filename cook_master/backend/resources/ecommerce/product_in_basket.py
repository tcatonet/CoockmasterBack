# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from resources.verification import token_required
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.ecommerce import ProductInBasket, Basket, Product


class ProductBasket(Resource):

    """ Product basket' endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    basket_id = Namespace(name='basket_id', default=0, dest="basket_id", action='store', type=int)
    product_id = Namespace(name='product_id', default=0, dest="product_id", action='store', type=str)
    quantity = Namespace(name='quantity', default=1, dest="quantity", action='store', type=str)
    prix = Namespace(name='price', default=1, dest="price", action='store', type=float)


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
            Post an ProductBasket
            :type user: User
            :params:    product_id: product id of the product basket to create
                        quantity: quantity of the product basket to create

            :return: ProductBasket json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.product_id)))
        parser.add_argument(**vars(self.__required__(self.quantity)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            basket = Basket.find_by_user_id(user_id=user.id)
            if not basket:
                abort(405, 'Basket could not be found')

            product = Product.find_by_id(id=data['product_id'])
            if not product:
                abort(405, 'Product could not be found')

            if product.stock >= int(data['quantity']):
                prix=float(data['quantity'])*product.prix
                product_in_basket = ProductInBasket(basket_id=basket.id, product_id=data['product_id'], quantity=data['quantity'], prix=prix)
            else:
                abort(400, 'Max quantity execeed')
 
            try:
                product_in_basket.add_to_db()
                product_in_basket_json = product_in_basket.json()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred adding the product to the basket')
               
            else:
                response = current_app.response_class(response=json.dumps(product_in_basket_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def patch(self, user): 
        """
            Patch an ProductBasket
            :type user: User
            :params:    id: id of the product basket to patch
                        quantity: quantity of the product basket to patch
            
            :return: ProductBasket json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__required__(self.quantity)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            basket = Basket.find_by_user_id(user_id=user.id)
            if not basket:
                abort(405, 'Basket could not be found')

            product_in_basket = ProductInBasket.find_by_id(id=data['id'], basket_id=basket.id)
            if not product_in_basket:
                abort(405, 'Product in basket could not be found')

            product = Product.find_by_id(id=product_in_basket.product_id)
            if not product:
                abort(405, 'Product could not be found')
            
            if product.stock < int(data['quantity']):
                abort(422, 'Max quantity execeed')

            try:
                keys_to_patch = dict() 
                keys_to_patch['quantity'] = data['quantity']
                keys_to_patch['prix'] = float(data['quantity'])*product.prix
                product_in_basket.patch_in_db(keys_to_patch)
                product_in_basket_json = product_in_basket.json()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred updating the product to the basket')

            else:
                response = current_app.response_class(response=json.dumps(product_in_basket_json), status=201,
                                                    mimetype='application/json')
                return response
        

    @token_required
    def delete(self, user): 
        """
            Patch an ProductBasket
            :type user: User
            :params:    id: id of the product basket to delete
            
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
            basket = Basket.find_by_user_id(user_id=user.id)
            if not basket:
                abort(405, 'Basket could not be found')

            try:
                product_in_basket = ProductInBasket.find_by_id(id=data['id'], basket_id=basket.id)
                product_in_basket.remove_from_db()
            
            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the product to the basket')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='product in basket deleted')), status=201,
                                                    mimetype='application/json')
                return response