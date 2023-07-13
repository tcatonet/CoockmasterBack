# BRAIZET Rémi
# Version 1.4

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

import json
from _datetime import datetime
import uuid

 
class CategorieContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    content_aggregate = db.relationship("ContentAggregate", back_populates="categorie_content")

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_categorie = dict(id=self.id, name=self.name)
        return json_categorie

    def all_json(categorie_list): 
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_categorie = []
        for categorie in categorie_list:
            obj = dict(id=categorie.id, name=categorie.name)
            json_categorie.append(obj)

        return json_categorie
    
    
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
    def find_all(cls):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel. 
        """
         
        return cls.query.filter_by().all()


class ContentAggregate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.String(5000))
    
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie_content.id'))
    categorie_content = db.relationship("CategorieContent", back_populates="content_aggregate")
    content = db.relationship("Content", back_populates="content_aggregate")
 
    def json(self, json_categorie, json_content_list):
        """ 
        Converts this store and all its items to JSON.
 
        :return: this store and all its items.
        :rtype: JSON. 
        """
        obj = dict(id=self.id, title=self.title, description=self.description, categorie=json_categorie, contents=json_content_list)
        return obj

    def all_json(content_aggregate_list): 
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_content_aggregate = []
        for content_aggregate in content_aggregate_list:
            obj = dict(id=content_aggregate.id, title=content_aggregate.title, description=content_aggregate.description, categorie_id=content_aggregate.categorie_id)
            json_content_aggregate.append(obj)

        return json_content_aggregate
    
    
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
    def find_all(cls, page):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user. 
            :rtype: UserModel.
        """

        request=cls.query.filter_by().order_by(ContentAggregate.date_creation.desc())
        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        return res
 

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    content = db.Column(db.String(5000))
    rank = db.Column(db.Integer)

    content_aggregate_id = db.Column(db.Integer, db.ForeignKey('content_aggregate.id'))
    content_aggregate = db.relationship("ContentAggregate", back_populates="content")

    def json(self):
        """ 
        Converts this store and all its items to JSON.
 
        :return: this store and all its items.
        :rtype: JSON. 
        """
        obj = dict(id=self.id, rank=self.rank, title=self.title, content=self.content)
        return obj

    def all_json(content_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_content = []
        for content in content_list:
            obj = dict(id=content.id, rank=content.rank, title=content.title, content=content.content)
            json_content.append(obj)

        return json_content
     
    
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
    def find_by_aggregate_content_id(cls, content_aggregate_id):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         
        return cls.query.filter_by(content_aggregate_id=content_aggregate_id).order_by(Content.rank.asc()).all()


    @classmethod
    def find_all(cls):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         
        return cls.query.filter_by().all()
    
