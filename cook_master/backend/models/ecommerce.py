# BRAIZET Rémi
# Version 1.4

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import json
from _datetime import datetime
import uuid


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    stock = db.Column(db.Integer)
    prix = db.Column(db.Float)
    note = db.Column(db.Float)

    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    store = db.relationship("Store", back_populates="products")
    product_in_baskets = db.relationship('ProductInBasket', back_populates="product")
    products_in_order = db.relationship('ProductInOrder', back_populates="product")

    def __init__(self, store_id, name, description, stock, prix):
        self.store_id = store_id
        self.name = name
        self.description = description
        self.stock = stock
        self.prix = prix

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(store_id=self.store_id, id=self.id, name=self.name, description=self.description, stock=self.stock, prix=self.prix)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()

    def patch_in_db(self, patch_values):
        """
            Update this basket in the DB.
        """
        num_rows_updated = self.query.filter_by(id=self.id).update(patch_values)
        db.session.commit()
        return num_rows_updated

    @classmethod
    def find_by_name(cls, name):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(name=name).first()
    
    
    @classmethod
    def get_all_from_basket(cls, product_in_baskets):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        res = []
        for p in product_in_baskets:
            res.append(cls.query.filter_by(id=p.product_id).first())
        return res


    @classmethod
    def find_by_store_id(cls, store_id):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(store_id=store_id)


    def remove_from_db(self):
        """
            Deletes this user from the DB.
        """
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def find_by_id(cls, _id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(id=_id).first()



class ProductInBasket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'))
    basket = db.relationship("Basket", back_populates="products")
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="product_in_baskets")
    quantity = db.Column(db.Integer)
    prix = db.Column(db.Float)

    def __init__(self, basket_id, product_id, quantity, prix=0.0):
        self.basket_id = basket_id
        self.product_id = product_id
        self.quantity = quantity
        self.prix = prix

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, basket_id=self.basket_id, product_id=self.product_id, quantity=self.quantity, prix=self.prix)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()

    def patch_in_db(self, patch_values):
        """
            Update this basket in the DB.
        """
        num_rows_updated = self.query.filter_by(id=self.id).update(patch_values)
        db.session.commit()
        return num_rows_updated

    def remove_from_db(self):
        """
            Deletes this user from the DB.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id, basket_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(id=id, basket_id=basket_id).first()



    @classmethod
    def get_all(cls, basket_id):
        """
            Selects a store from the DB and returns it.

            :param name: the username of the user.
            :type name: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(basket_id=basket_id)

class ProductInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="products_in_order")

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="products_in_order")
    quantity = db.Column(db.Integer)
    prix = db.Column(db.Float)

    def __init__(self, order_id, product_id, quantity, prix):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.prix = prix


    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()
 

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    products = db.relationship('ProductInBasket', back_populates='basket')
    prix = db.Column(db.Integer)

    def __init__(self, user_id):
        self.user_id = user_id

    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()

    def patch_in_db(self, patch_values):
        """
            Update this basket in the DB.
        """
        num_rows_updated = self.query.filter_by(id=self.id).update(patch_values)
        db.session.commit()
        return num_rows_updated


    def all_json(self, product_in_baskets):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """

        products_list = {'products': []}

        for product in product_in_baskets:

            obj = dict(id=product.id, quantity=product.quantity)
            products_list['products'].append(obj)
        return products_list

    @classmethod
    def find_by_user_id(cls, user_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def delete_all_from_basket(cls, product_in_baskets):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        for p in product_in_baskets:
            db.session.delete(p)
        
        db.session.commit()


class Store(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    products = db.relationship('Product', back_populates='store')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, name=self.name)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj


    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()

    def patch_in_db(self, patch_values):
        """
            Update this basket in the DB.
        """
        num_rows_updated = self.query.filter_by(id=self.id).update(patch_values)
        db.session.commit()
        return num_rows_updated
    

    def all_json(self, products):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """

        products_list = {'products': []}

        for product in products:

            obj = dict(id=product.id, name=product.name, description=product.description, stock=product.stock, prix=product.prix)
            products_list['products'].append(obj)
        return products_list

    @classmethod
    def find_by_name(cls, name):
        """
            Selects a store from the DB and returns it.

            :param name: the username of the user.
            :type name: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(name=name).first()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prix = db.Column(db.Integer)
    products_in_order = db.relationship('ProductInOrder', back_populates="order")
    #order_list = db.relationship('OrderList', back_populates="order")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    status = db.Column(db.String(50), unique=True)


    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self) 
        db.session.commit() 


    def patch_in_db(self, patch_values):
        """
            Update this basket in the DB.
        """
        num_rows_updated = self.query.filter_by(id=self.id).update(patch_values)
        db.session.commit()
        return num_rows_updated
    

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, prix=self.prix)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj
    

    # def all_json(self, order_list):
    #     """
    #     Converts this store and all its items to JSON.

    #     :return: this store and all its items. 
    #     :rtype: JSON.
    #     """

    #     orders_list = {'orders': []}

    #     for order in order_list:

    #         obj = dict(id=order.id, price=order.price)
    #         orders_list['orders'].append(obj)
    #     return orders_list
 
 
    # def json(self, product_list):
    #     """
    #     Converts this store and all its items to JSON.

    #     :return: this store and all its items.
    #     :rtype: JSON.
    #     """

    #     products_list = {'products': []}

    #     for product in product_list:

    #         obj = dict(id=product.id, price=product.price)
    #         products_list['products'].append(obj)
    #     return products_list


    @classmethod
    def get_all(cls, user_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(user_id=user_id).all()


    @classmethod
    def find_one_by_id(cls, id, user_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(id=id, user_id=user_id).first()
    

# class OrderList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     order = db.relationship("Order", back_populates="products")

#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     user = db.relationship("User", back_populates="orders")
#     quantity = db.Column(db.Integer)

#     @classmethod
#     def find_by_user_id(cls, user_id):
#         """
#             Selects a user from the DB and returns it.

#             :param _id: the id of the user.
#             :type _id: int
#             :return: a user.
#             :rtype: UserModel.
#         """
        
#         return cls.query.filter_by(user_id=user_id)



#     def all_json(self, orders):
#         """
#         Converts this store and all its items to JSON.

#         :return: this store and all its items.
#         :rtype: JSON.
#         """

#         orders_list = {'orders': []}

#         for order in orders:

#             obj = dict(id=order.id, price=order.price)
#             orders_list['orders'].append(obj)
#         return orders_list
