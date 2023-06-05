# BRAIZET Rémi
# Version 1.4

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

import json
from _datetime import datetime
import uuid


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    adress = db.Column(db.String(50))

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

    def all_json(room_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_room = []
        for room in room_list:
            obj = dict(id=room.id, city=room.city, postcode=room.postcode, adress=room.adress)
            json_room.append(obj)

        response = jsonify(json.dumps(json_room, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_room
    
    
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


class Prestataire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    activite = db.Column(db.String(50))
    description = db.Column(db.String(50))

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, nom=self.nom, prenom=self.prenom, activite=self.activite, description=self.description)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def all_json(prestataire_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_prestataire = []
        for prestataire in prestataire_list:
            obj = dict(id=prestataire.id, nom=prestataire.nom, prenom=prestataire.prenom, activite=prestataire.activite, description=prestataire.description)
            json_prestataire.append(obj)

        response = jsonify(json.dumps(json_prestataire, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_prestataire
    
    
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