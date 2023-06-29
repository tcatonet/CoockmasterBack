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
    capacity = db.Column(db.Integer)

    room_in_event = db.relationship('RoomInEvent', back_populates="room")

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, city=self.city, postcode=self.postcode, adress=self.adress, capacity=self.capacity)
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
            obj = dict(id=room.id, city=room.city, postcode=room.postcode, adress=room.adress, capacity=room.capacity)
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
    lastname = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    activite = db.Column(db.String(50))
    description = db.Column(db.String(50))
    email = db.Column(db.String(50))

    prestataire_in_event = db.relationship('PrestataireInEvent', back_populates="prestataire")

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, lastname=self.lastname, firstname=self.firstname, activite=self.activite, description=self.description)
        return obj


    def json_admin(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, lastname=self.lastname, firstname=self.firstname, email=self.email, activite=self.activite, description=self.description)
        return obj


    def all_json(prestataire_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_prestataire = []
        for prestataire in prestataire_list:
            obj = dict(id=prestataire.id, lastname=prestataire.lastname, firstname=prestataire.firstname, activite=prestataire.activite, description=prestataire.description)
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
    def find_by_email(cls, email):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         
        return cls.query.filter_by(email=email).first()

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
    

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_mandatory = db.Column(db.Boolean())
    prestataire_mandatory = db.Column(db.Boolean())

    event = db.relationship("Event", back_populates="categorie")

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, room_mandatory=self.room_mandatory, prestataire_mandatory=self.prestataire_mandatory)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def all_json(categorie_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_categorie = []
        for categorie in categorie_list:
            obj = dict(id=categorie.id, room_mandatory=categorie.room_mandatory, prestataire_mandatory=categorie.prestataire_mandatory)
            json_categorie.append(obj)

        response = jsonify(json.dumps(json_categorie, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
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


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(1000))
    public = db.Column(db.Boolean(), default=False)

    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    categorie = db.relationship("Categorie", back_populates="event")

    rooms = db.relationship('RoomInEvent', back_populates="event")
    prestataires = db.relationship('PrestataireInEvent', back_populates="event")
    event_list_user = db.relationship('EventUserSubscription', back_populates="event")
 
    def json(self, prestataire, room, categorie=None):
        """ 
        Converts this store and all its items to JSON.
 
        :return: this store and all its items.
        :rtype: JSON. 
        """
        res_cat = categorie if categorie else self.categorie_id
        obj = dict(id=self.id, name=self.name, description=self.description, prestataire=prestataire, room=room, categorie=res_cat, public=self.public)
        return obj

    def all_json(event_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_event = []
        for event in event_list:
            obj = dict(id=event.id, prestataire_id=event.prestataire_id, room_id=event.room_id, categorie_id=event.categorie_id)
            json_event.append(obj)

        response = jsonify(json.dumps(json_event, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_event
    
    
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
    

class RoomInEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="room_in_event")

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="rooms")

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id 

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, room_id=self.room_id, event_id=self.event_id)
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
    def find_by_event_id(cls, event_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(event_id=event_id).all()
    
    @classmethod
    def find_by_room_event_id(cls, room_id, event_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(room_id=room_id, event_id=event_id).first()

    @classmethod
    def find_by_room_id(cls, room_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(room_id=room_id).all()

    @classmethod
    def get_all(cls):
        """
            Selects a store from the DB and returns it.

            :param name: the username of the user.
            :type name: str
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by().all()


class PrestataireInEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prestataire_id = db.Column(db.Integer, db.ForeignKey('prestataire.id'))
    prestataire = db.relationship("Prestataire", back_populates="prestataire_in_event")
    
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="prestataires")

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, prestataire_id=self.prestataire_id, event_id=self.event_id)
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
    def find_by_prestataire_id(cls, prestataire_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user. 
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(prestataire_id=prestataire_id).all()


    @classmethod
    def find_by_prestataire_event_id(cls, prestataire_id, event_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(prestataire_id=prestataire_id, event_id=event_id).first()

 
    @classmethod
    def find_by_event_id(cls, event_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(event_id=event_id).all()
    
    @classmethod
    def get_all(cls):
        """
            Selects a store from the DB and returns it.

            :param name: the username of the user.
            :type name: str
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by()


class EventUserSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship("Event", back_populates="event_list_user")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="event_list_user")

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, event_id=self.event_id, user_id=self.user_id)
        response = jsonify(json.dumps(obj, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return obj

    def add_to_db(self):
        """
            Inserts this user in the DB. 
        """
        db.session.add(self)
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

    def all_json(event_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_event = []
        for event in event_list:
            obj = dict(id=event.id, name=event.name, description=event.description)
            json_event.append(obj)

        response = jsonify(json.dumps(json_event, ensure_ascii=False))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return json_event