# BRAIZET Rémi
# Version 1.4

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

import json
from _datetime import datetime
import uuid


class User(db.Model):
    """User model."""

    __tablename__ = 'user'
    # items = db.relationship('projects', lazy='dynamic')
  
    id = db.Column(db.Integer, primary_key=True, unique=True)
    basket = db.relationship("Basket",  uselist=False, backref="user")
    orders = db.relationship('Order', back_populates='user')

    user_level = db.Column(db.Integer)
    code = db.Column(db.Integer)
    username = db.Column(db.String(80))
    password = db.Column(db.String(256))
    email = db.Column(db.String(80), unique=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow())
    verified = db.Column(db.String(36))  # stores an uuid
    phone = db.Column(db.String(10), default='00.00.00.00.00')
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email_validate = db.Column(db.Boolean)

    # billing_address = db.Column(db.String(256))

    def __init__(self, username, password, email, level=0, phone='', first_name='', last_name='', code=10000, email_validate=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.level = level
        self.registered_on = datetime.utcnow()
        self.verified = str(uuid.uuid4())

        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.code = code
        self.email_validate = email_validate
        self.basket = None

        # self.billing_address = None
        
    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(username=self.username, password=self.password, email=self.email, id=self.id,
                   phone=self.phone, first_name=self.first_name, last_name=self.last_name, verified=self.verified,
                   registered_on=self.registered_on.strftime('%m/%d/%Y'))
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    @classmethod
    def find_by_email(cls, email):
        """
            Selects a user from the DB and returns it.

            :param _email: the username of the user.
            :type _email: str
            :return: a user.
            :rtype: UserModel.
        """

        return cls.query.filter_by(email=email).first()

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

    @classmethod
    def find_by_registration_token(cls, _token):
        """
            Selects a user from the DB and returns it.

            :param _token: the creation token of the user.
            :type _token: string that represent an uuid4
            :return: a user.
            :rtype: UserModel.
        """
        
        return cls.query.filter_by(verified=_token).first()
    
    def add_to_db(self):
        """
            Inserts this user in the DB.
        """
        db.session.add(self)
        db.session.commit()
    
    def patch_in_db(self, patch_values):
        """
            Update this user in the DB.
        """

        num_rows_updated = self.query.filter_by(email=self.email).update(patch_values)
        db.session.commit()
        return num_rows_updated


    def remove_from_db(self):
        """
            Deletes this user from the DB.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_users(cls):
        return len(cls.query.all())

    @classmethod
    def all_json_order(self, order_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items. 
        :rtype: JSON.
        """

        orders_list = {'orders': []}
 
        for order in order_list:

            obj = dict(id=order.id, prix=order.prix)
            orders_list['orders'].append(obj)
        return orders_list



    def register(self):
        num_rows_updated = self.query.filter_by(email=self.email).update(dict(verified=True))
        db.session.commit()
        return num_rows_updated
