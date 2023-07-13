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

    product_categorie_id = db.Column(db.Integer, db.ForeignKey('product_categorie.id'))
    product_categorie = db.relationship("ProductCategorie", back_populates="products")

    product_in_baskets = db.relationship('ProductInBasket', back_populates="product")
    products_in_order = db.relationship('ProductInOrder', back_populates="product")
    avis = db.relationship('Avis', back_populates="product")
    date_creation = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, store_id, name, description, stock, prix, product_categorie_id):
        self.store_id = store_id
        self.name = name
        self.description = description
        self.stock = stock
        self.prix = prix
        self.product_categorie_id = product_categorie_id

    def __repr__(self): 
        return "<TableName(id='%s')>" % self.id 
 
    def json(self, product_avis):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(store_id=self.store_id, product_categorie_id=self.product_categorie_id, id=self.id, name=self.name, note=self.note, description=self.description, stock=self.stock, prix=self.prix, product_avis=product_avis)
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


    @classmethod
    def find_by_categorie_id(cls, store_id, product_categorie_id):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(store_id=store_id, product_categorie_id=product_categorie_id)


    @classmethod
    def find_by_note_min(cls, store_id, note):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """ 
        return cls.query.filter(store_id=store_id).filter(note>note)

    @classmethod
    def find_by_note_min_max_price(cls, store_id, min_price, max_price):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(store_id=store_id).filter(Product.prix>=min_price).filter(Product.prix<=max_price)

    @classmethod
    def find_by_note_min_price(cls, store_id, min_price):
        """
            Selects a user from the DB and returns it. 

            :param _email: the username of the user.
            :type _email: str
            :return: a user. 
            :rtype: UserModel.
        """
        return cls.query.filter_by(store_id=store_id).filter(Product.prix>=min_price)
    
    @classmethod 
    def find_by_note_max_price(cls, store_id, max_price):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(store_id=store_id).filter(Product.prix<=max_price)
    
    @classmethod
    def find_by_product_categorie_id(cls, store_id, product_categorie_id, min_price, max_price, min_note, page):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        request = cls.query.filter_by(store_id=store_id)

        if product_categorie_id:
            request=request.filter(Product.product_categorie_id==product_categorie_id).order_by(Product.date_creation.desc())

        if min_price:  
            request=request.filter(Product.prix>=min_price).order_by(Product.prix.asc())

        if max_price:
            request=request.filter(Product.prix<=max_price).order_by(Product.prix.asc())
            
        if min_note:
            request=request.filter(Product.note>=min_note).order_by(Product.note.desc())
 

        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        return res

 
    @classmethod
    def find_by_product_by_filter(cls, product_categorie_id):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(product_categorie_id=product_categorie_id)


    def remove_from_db(self):
        """
            Deletes this user from the DB.
        """
        db.session.delete(self)
        db.session.commit() 


    @classmethod
    def find_by_id(cls, id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(id=id).first()


class ProductCategorie(db.Model):
    __tablename__ = 'product_categorie'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True)
    products = db.relationship('Product', back_populates='product_categorie')

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
    
    def all_json(product_categorie_list): 
        """ 
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_product_categorie = []
        for product_categorie in product_categorie_list:
            obj = dict(id=product_categorie.id, name=product_categorie.name)
            json_product_categorie.append(obj)

        response = jsonify(json.dumps(json_product_categorie, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_product_categorie
    
    @classmethod
    def find_by_id(cls, id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all(cls):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        return cls.query.filter_by().all()


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


class Avis(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    product_in_order_id = db.Column(db.Integer, db.ForeignKey('product_in_order.id'))
    product_in_order = db.relationship("ProductInOrder", back_populates="avis")

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="avis")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="avis")
    username = db.Column(db.String(100))

    note = db.Column(db.Integer)
    comentary = db.Column(db.String(1000)) 

    def json(self, user_name):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """ 
        obj = dict(id=self.id, user_id=self.user_id, user_name=user_name,  note=self.note, comentary=self.comentary, product_id=self.product_id, product_in_order_id=self.product_in_order_id, )
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def all_json(avis_list): 
        """ 
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_avis = []
        for avis in avis_list:
            obj = dict(id=avis.id, user_id=avis.user_id, user_name=avis.username, note=avis.note, comentary=avis.comentary, product_id=avis.product_id, product_in_order_id=avis.product_in_order_id, )
            json_avis.append(obj)

        response = jsonify(json.dumps(json_avis, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_avis
    

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
    def find_by_id(cls, id, user_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """  
         
        return cls.query.filter_by(id=id, user_id=user_id).first()

    @classmethod
    def find_all(cls, user_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user. 
            :rtype: UserModel.
        """
         
        return cls.query.filter_by(user_id=user_id)
    

    @classmethod
    def find_by_order_and_product(cls, product_in_order_id, product_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """  
        return cls.query.filter_by(product_in_order_id=product_in_order_id, product_id=product_id).first()
    
    @classmethod
    def find_all_by_product_id(cls, product_id, page=1):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(product_id=product_id)


class ProductInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order", back_populates="products_in_order")

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship("Product", back_populates="products_in_order")

    avis = db.relationship("Avis", back_populates="product_in_order")

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

    @classmethod
    def find_by_order_id(cls, order_id):
        """
            Inserts this user in the DB.
        """
        return cls.query.filter_by(order_id=order_id)


 

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

            obj = dict(id=product.id, product_categorie_id=product.product_categorie_id,  note=product.note, name=product.name, description=product.description, stock=product.stock, prix=product.prix)
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
    

    @classmethod
    def find_by_id(cls, id):
        """
            Selects a store from the DB and returns it.

            :param name: the username of the user.
            :type name: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(id=id).first()



class Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    adress = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="adress")
    orders = db.relationship('Order', back_populates='adress')

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, city=self.city, postcode=self.postcode, adress=self.adress)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def all_json(adress_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_adress = []
        for adress in adress_list:
            obj = dict(id=adress.id, city=adress.city, postcode=adress.postcode, adress=adress.adress)
            json_adress.append(obj)

        response = jsonify(json.dumps(json_adress, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_adress
    
    
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
    def find_by_id(cls, id, user_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """  
        return cls.query.filter_by(id=id, user_id=user_id).first()

    @classmethod
    def find_all(cls, user_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         
        return cls.query.filter_by(user_id=user_id)
     



class Order(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="orders")
    adress_id = db.Column(db.Integer, db.ForeignKey('adress.id'))
    adress = db.relationship("Adress", back_populates="orders")
    id = db.Column(db.Integer, primary_key=True)
    prix = db.Column(db.Integer)
    products_in_order = db.relationship('ProductInOrder', back_populates="order")
    status = db.Column(db.String(50), unique=True)
    invoice = db.Column(db.String(50), unique=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow())

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
    

    def json(self, products_in_order, adress):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items. 
        :rtype: JSON.
        """
        order_adress = dict(city=adress.city, postcode=adress.postcode, adress=adress.adress)

        json_products_in_order = []
        for product_in_order in products_in_order:
            obj = dict(id=product_in_order.id, 
                       order_id=product_in_order.order_id, 
                       product_id=product_in_order.product_id, 
                       quantity=product_in_order.quantity, 
                       prix=product_in_order.prix)
            
            json_products_in_order.append(obj)

        obj = dict(id=self.id, prix=self.prix, status=self.status, adress=order_adress, products_in_order=json_products_in_order)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj
  

    @classmethod
    def find_all(cls, user_id, page):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.   
            :type _id: int 
            :return: a user.
            :rtype: UserModel. 
        """
        
        request=cls.query.filter_by(user_id=user_id).order_by(Order.date_creation.desc())
        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        return res
 
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