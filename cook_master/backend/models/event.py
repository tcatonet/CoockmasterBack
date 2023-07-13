# BRAIZET Rémi
# Version 1.4

from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

import json
from datetime import datetime
import uuid
from utils.global_config import PRIVATE


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    postcode = db.Column(db.String(50))
    adress = db.Column(db.String(50))
    capacity = db.Column(db.Integer)

    room_in_event = db.relationship('RoomInEvent', back_populates="room")
    room_in_sub = db.relationship('EventUserSubscription', back_populates="room")

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
    def find_all(cls, page):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """

        request=cls.query.filter_by().all()
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
    def find_all_by_date(cls, page, date_start, date_end):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """

        request=cls.query.filter_by().all()
        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        room_list = []
        for room in res:
            r = RoomInEvent.find_all_by_date(cls, room_id=room.id, date_start=date_start, date_end=date_end)
            if not r:
                room_list.append(r)

        return room_list


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
    def find_all(cls, page):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         

        request=cls.query.filter_by().all()
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
    def find_all_by_date(cls, page, date_start, date_end):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """

        request=cls.query.filter_by().all()
        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        prestatiare_list = []
        for prestatiare in res:
            r = PrestataireInEvent.find_all_by_date(cls, prestataire_id=prestatiare.id, date_start=date_start, date_end=date_end)
            if not r:
                prestatiare_list.append(r)

        return prestatiare_list
    

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
    total_capacity = db.Column(db.Integer)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)

    status=db.Column(db.Boolean(), default=False)  
    access = db.Column(db.Boolean(), default=True)

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
        obj = dict(id=self.id, name=self.name, description=self.description, date_start=self.date_start, date_end=self.date_end, prestataire=prestataire, room=room, categorie=res_cat, access=self.access)
        return obj

    def all_json(event_list, prestataire, room, categorie=None):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_event = []
        for event in event_list:
            categorie = Categorie.find_by_id(id=event.categorie_id) 
            json_categorie = categorie.json()
            prestataire_in_event_list = PrestataireInEvent.find_by_event_id(event_id=event.id)
            json_prestataire_list = []

            if prestataire_in_event_list:
                for prestataire in prestataire_in_event_list:
                    prestataire = Prestataire.find_by_id(id=prestataire.prestataire_id)
                    json_prestataire= prestataire.json()
                    json_prestataire_list.append(json_prestataire)
            else:
                json_prestataire_list={}
 
            room_in_event_list = RoomInEvent.find_by_event_id(event_id=event.id)
            json_room_list = []

            if room_in_event_list:
                for room in room_in_event_list:
                    room = Room.find_by_id(id=room.room_id)
                    json_room=room.json()
                    json_room_list.append(json_room)

            else:
                json_room_list={}

            obj = dict(id=event.id, date_start=event.date_start, date_end=event.date_end,  prestataire=json_prestataire_list, room=json_room_list, categorie=json_categorie)
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
    def find_all(cls, page):
        """ 
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
         
        request=cls.query.filter_by(Event.access != PRIVATE).all()
        limit_min=(page-1)*20-1

        if limit_min<0:
            limit_min =0
 
        res = request[limit_min:page*20]

        if not res and request:
            request_len=len(request)
            x_last_product=request_len%20-1
            res = request[x_last_product:request_len]

        return res


class RoomInEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="room_in_event")
    current_capacity = db.Column(db.Integer, default=0)
    max_capacity = db.Column(db.Integer)
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)

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
    def find_by_event_id_room_id(cls, event_id, room_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.all
        """
        return cls.query.filter_by(event_id=event_id, room_id=room_id).first()

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
    def find_all_by_date(cls, room_id, date_start, date_end):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        res = cls.query.filter(RoomInEvent.room_id==room_id)\
            .filter(RoomInEvent.date_start>date_start, RoomInEvent.date_start<date_end)\
            .all()
        
        res2 = cls.query.filter(RoomInEvent.room_id==room_id)\
                .filter(RoomInEvent.date_end>date_start, RoomInEvent.date_end<date_end)\
                .all()
        
        res3 = cls.query.filter(RoomInEvent.room_id==room_id)\
                .filter(RoomInEvent.date_start<date_start, RoomInEvent.date_end>date_end)\
                .all()



        return res+res2+res3


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
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)

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
    def find_all_by_date(cls, prestataire_id, date_start, date_end):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        res = cls.query.filter(PrestataireInEvent.prestataire_id==prestataire_id)\
            .filter(PrestataireInEvent.date_start>date_start, PrestataireInEvent.date_start<date_end)\
            .all()
        
        res2 = cls.query.filter(PrestataireInEvent.prestataire_id==prestataire_id)\
                .filter(PrestataireInEvent.date_end>date_start, PrestataireInEvent.date_end<date_end)\
                .all()
        
        res3 = cls.query.filter(PrestataireInEvent.prestataire_id==prestataire_id)\
                .filter(PrestataireInEvent.date_start<date_start, PrestataireInEvent.date_end>date_end)\
                .all()

        return res+res2+res3


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
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="room_in_sub")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="event_list_user")

    def __init__(self, user_id, event_id, room_id):
        self.user_id = user_id
        self.event_id = event_id
        self.room_id = room_id

    def json(self):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        obj = dict(id=self.id, event_id=self.event_id, user_id=self.user_id)
        return obj

    def add_to_db(self):
        """
            Inserts this user in the DB. 
        """
        db.session.add(self)
        db.session.commit()

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
    def find_by_user_id(cls, user_id):
        """
            Selects a user from the DB and returns it.

            :param _id: the id of the user.
            :type _id: int
            :return: a user.
            :rtype: UserModel.
        """
        return cls.query.filter_by(user_id=user_id).all()
    
    def all_json(event_list):
        """
        Converts this store and all its items to JSON.

        :return: this store and all its items.
        :rtype: JSON.
        """
        json_event = []
        for event in event_list:
            obj = dict(id=event.id, event=event.event_id)
            json_event.append(obj)

        return json_event