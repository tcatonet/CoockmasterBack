# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from resources.verification import token_required
from flask import abort, current_app
from flask_restful import Resource

from models.ecommerce import ProductInBasket, Basket, Product


class UserBasket(Resource):

    """ Basket' endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
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
    def get(self, user):
        """
            Get a basket
            :type user: User
        
            :return: basket json
            :rtype: application/json.
        """
        basket = Basket.find_by_user_id(user_id=user.id)

        if not basket:
            abort(405, 'Basket could not be found')
        
        product_in_baskets = ProductInBasket.get_all(basket_id=basket.id)
        if not product_in_baskets:
            abort(405, 'Product in basket could not be found')
        
        products = Product.get_all_from_basket(product_in_baskets= product_in_baskets)

        try: 

            basket_price=0
            for p in products:
                basket_price+=p.prix

            keys_to_patch = dict()
            keys_to_patch['prix'] = float(basket_price)
            basket.patch_in_db(keys_to_patch)

            json_product_in_baskets = basket.all_json(product_in_baskets=product_in_baskets)
            response = current_app.response_class(response=json.dumps(json_product_in_baskets), status=200,
                                                      mimetype='application/json')
            return response
        
        except ValueError:
            abort(404, str(ValueError))


    @token_required
    def delete(self, user):
        """
            Delete a basket
            :type user: User
        
            :return: str
            :rtype: application/json.
        """

        basket = Basket.find_by_user_id(user_id=user.id)
        if not basket:
            abort(405, 'Basket could not be found')

        try:
            product_in_baskets = ProductInBasket.get_all(basket_id= basket.id)
            Basket.delete_all_from_basket(product_in_baskets= product_in_baskets)
            response = current_app.response_class(response=json.dumps(dict(message='basket deleted')), status=200,
                                                      mimetype='application/json')
            return response 
        
        except ValueError:
            abort(404, str(ValueError))