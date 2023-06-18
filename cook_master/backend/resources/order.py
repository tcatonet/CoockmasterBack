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

from models.ecommerce import Basket, Order, ProductInBasket, ProductInOrder, Product, Adress

DELETE='delete'


class UserOrder(Resource):
 
    """ Order's endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
    status = Namespace(name='status', default=0, dest="status", action='store', type=str)
    adress_id = Namespace(name='adress_id', default=0, dest="adress_id", action='store', type=int)

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
    def patch(self, user):
        """
            Patch an order
            :type user: User
            :params:    id: order id to patch
                        status: new status of the order
                        
            :return: order data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__required__(self.status)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            order = Order.find_one_by_id(id=data['id'], user_id=user.id)
            if not order:
                abort(404, 'Order could not be found')

            keys_to_patch = dict()
            keys_to_patch['status'] = data['status']

            try:
                order.patch_in_db(keys_to_patch)
            
            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred updating the order')

            adress= Adress.find_by_id(id=order.adress_id, user_id=user.id)
            if not adress:
                abort(404, 'Adress could not be found')

            products_in_order = ProductInOrder.find_by_order_id(order_id=order.id)
            if not products_in_order:
                abort(404, 'Order product could not be found')

            order_json = order.json(products_in_order=products_in_order, adress=adress) 
            response = current_app.response_class(response=json.dumps(order_json), status=200,
                                                        mimetype='application/json')
            return response


    @token_required
    def delete(self, user):
        """
            Delete an order
            :type user: User
            :params:    id: order id to delete

            :return: order data.
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
            order = Order.find_one_by_id(id=data['id'], user_id=user.id)
            if not order:
                abort(404, 'Order could not be found')

            keys_to_patch = dict()
            keys_to_patch['status'] = DELETE

            try: 
                order_data = order.patch_in_db(keys_to_patch)

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the order')

            else:
                response = current_app.response_class(response=json.dumps(order_data), status=200,
                                                        mimetype='application/json')
                return response


    @token_required
    def post(self, user):
        """ 
            Post an order
            :params:    id: order id to delete

            :return: order json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.adress_id)))

        try:
            data = parser.parse_args()
            del parser
            
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body22')
        
        else: 
            basket = Basket.find_by_user_id(user_id=user.id)
            if not basket:
                abort(404, 'Basket could not be found')

            order = Order(user_id=user.id, adress_id=data['adress_id'])

            order.add_to_db()
            products_in_basket = ProductInBasket.get_all(basket_id=basket.id)
            if not products_in_basket:
                abort(406, 'Products in basket could not be found')

            po = []

            nb_products = 0
            for p in products_in_basket:
                nb_products+=1
                product = Product.find_by_id(_id=p.product_id)
                if not product:
                    abort(404, 'Product could not be found')

                if product.stock < p.quantity:
                    abort(400, 'Max quantity execeed')

            if not nb_products:
                abort(400, 'Empty basket')

            order_prix = 0
            for p in products_in_basket:
                product_in_order = ProductInOrder(order_id=order.id, product_id=p.id, quantity=p.quantity, prix=float(p.prix))

                product_in_order.add_to_db() 
                product = Product.find_by_id(_id=p.product_id)
                if not product:
                    abort(408, 'Product could not be found')

                keys_to_patch = dict()
                keys_to_patch['stock'] = product.stock - p.quantity
                product.patch_in_db(keys_to_patch)
                order_prix += p.prix
                po.append(product_in_order)

            keys_to_patch = dict()
            keys_to_patch['prix'] = float(order_prix)
            order.patch_in_db(keys_to_patch)
                
            adress= Adress.find_by_id(id=order.adress_id, user_id=user.id)
            if not adress:
                    abort(404, 'Adress could not be found')

            products_in_order = ProductInOrder.find_by_order_id(order_id=order.id)
            if not products_in_order:
                    abort(404, 'Product order could not be found')

            order_json = order.json(products_in_order=products_in_order, adress=adress) 

            response = current_app.response_class(response=json.dumps(order_json), status=200,
                                                        mimetype='application/json')
            return response



    @token_required
    def get(self, user):
        """
            Get an order 
            :type user: User
            :params:    id: order id to get

            :return: order json data.
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
                order = Order.find_one_by_id(id=data['id'], user_id=user.id)
                if not order:
                    abort(404, 'Order could not be found')

                adress= Adress.find_by_id(id=order.adress_id, user_id=user.id)
                if not adress:
                    abort(404, 'Adress could not be found')

                products_in_order = ProductInOrder.find_by_order_id(order_id=order.id)
                if not products_in_order:
                    abort(404, 'Product order could not be found')
 
                order_json = order.json(products_in_order=products_in_order, adress=adress) 
                
            else:
                orders = Order.get_all(user_id=user.id)
                if not orders:
                    abort(404, 'Orders could not be found')

                order_json = user.all_json_order(order_list=orders)

            response = current_app.response_class(response=json.dumps(order_json), status=200,
                                                      mimetype='application/json')
            return response