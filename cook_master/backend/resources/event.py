# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Event
from models.event import Prestataire, Room, Categorie


class UserEvent(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
    description = Namespace(name='description', default=0, dest="description", action='store', type=str)

    categorie_id = Namespace(name='categorie_id', default=0, dest="categorie_id", action='store', type=int)

    room_id = Namespace(name='room_id', default=0, dest="room_id", action='store', type=int)
    prestataire_id = Namespace(name='prestataire_id', default=0, dest="prestataire_id", action='store', type=int)

 
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
    

    def post(self):
        """
            Post a Product
            :params:    name: name of the product to create
                        description: description of the product to create
                        stock: stock of the product to create
                        prix: prix of the product to create
                        store_id: store of the product to create

            :return: Product json data. 
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.name)))
        parser.add_argument(**vars(self.__required__(self.description)))
        parser.add_argument(**vars(self.__required__(self.categorie_id)))
        parser.add_argument(**vars(self.__optional__(self.room_id)))
        parser.add_argument(**vars(self.__optional__(self.prestataire_id)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:

            if 'room_id' not in data:
                data['room_id']=-1

            if 'prestataire_id' not in data:
                data['prestataire_id']=-1

            event = Event(name=data['name'], 
                          description=data['description'], 
                          categorie_id=data['categorie_id'], 
                          room_id=data['room_id'], 
                          prestataire_id=data['prestataire_id'])
            if not event:
                abort(405, 'Event could not be found')

            try:
                event.add_to_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the event')

            event_json = event.json() 
            response = current_app.response_class(response=json.dumps(event_json), status=201,
                                                mimetype='application/json')
            return response


    def get(self):
        """
            Get an Product
            :params:    name: name of the product to get

            :return: Product json data.
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

            if data['id']:
                event = Event.find_by_id(id=data['id'])

                prestataire = Prestataire.find_by_id(id=event.prestataire_id)
                categorie = Categorie.find_by_id(id=event.categorie_id)
                room = Room.find_by_id(id=event.room_id)

                json_prestataire= prestataire.json()
                json_categorie=categorie.json()
                json_room=room.json()


                json_event = event.json(json_prestataire=json_prestataire, json_categorie=json_categorie, json_room=json_room)
            
            else:
                event_list=Event.find_all()
                json_event = Event.all_json(event_list=event_list)

            if not event:
                abort(405, 'Event could not be found')
            
            try:
                response = current_app.response_class(response=json.dumps(json_event), status=200,
                                                      mimetype='application/json')
                return response

            except Exception as e:
                logging.error(e)
                abort(400, 'An error occurred retrieving the event')


    def delete(self):
        """
            Delete a Product
            :params:    name: nameof the product to delete

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
            event = Event.find_by_id(id=data['id'])
            if not event:
                abort(405, 'Event could not be found')

            event.remove_from_db()

        response = current_app.response_class(response=json.dumps(dict(message='event deleted')), status=204, mimetype='application/json')

        return response


    def patch(self):
        """
            Patch a Product
            :params:    name: name of the product to patch
                        description: description of the product to patch
                        stock: stock of the product to patch
                        prix: prix of the product to patch
                        store_id: store of the product to patch

            :return: Product json data 
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.name)))
        parser.add_argument(**vars(self.__optional__(self.description)))
        parser.add_argument(**vars(self.__optional__(self.prestataire_id)))
        parser.add_argument(**vars(self.__optional__(self.room_id)))

        try: 
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e) 
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '': 
                    keys_to_patch[key] = data[key]

            event = Event.find_by_id(id=data['id'])
            if not event:
                abort(404, dict(message='Event could not be found'))

            try:
                event.patch_in_db(keys_to_patch)
                
            except Exception as e:
                logging.error(e) 
                abort(405, dict(message='Cannot update vent'))

            response = current_app.response_class(response=json.dumps(dict(message='event udpated')), status=204, mimetype='application/json')
            return response