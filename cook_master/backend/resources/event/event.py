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
from models.event import Prestataire, Room, Categorie, RoomInEvent, PrestataireInEvent
from utils.global_config import ADMIN_LEVEL
from resources.verification import token_required


class UserEvent(Resource):

    """ Product endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    name = Namespace(name='name', default=0, dest="name", action='store', type=str)
    public = Namespace(name='public', default=False, dest="public", action='store', type=bool)

    description = Namespace(name='description', default=0, dest="description", action='store', type=str)

    categorie_id = Namespace(name='categorie_id', default=0, dest="categorie_id", action='store', type=int)

    room_id = Namespace(name='room_id', default=None, dest="room_id", action='store', type=list, location='json')
    prestataire_id = Namespace(name='prestataire_id', default=None, dest="prestataire_id", action='store', type=list, location='json')

 
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
    def post(self, user): 
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
        parser.add_argument(**vars(self.__optional__(self.public)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:

            if 'public' in data:
                if user.level != ADMIN_LEVEL:
                    data.pop('public')
            if data['name'] == '':
                abort(400, 'invalid name')
            if data['description'] == '':
                abort(400, 'invalid description')

            rooms=[]
            for room_id in data['room_id']:
                    room = Room.find_by_id(id=room_id)
                    if not room:
                        abort(405, 'Room could not be found')
                    else:
                        rooms.append(room.id) 

            prestataires=[]
            for prestataire_id in data['prestataire_id']:
                    prestataire = Prestataire.find_by_id(id=prestataire_id)
                    if not prestataire:
                        abort(405, 'Prestataire could not be found')
                    else:
                        prestataires.append(prestataire.id) 

            categorie = Categorie.find_by_id(id=data['categorie_id'])
            if not categorie:
                abort(405, 'Categorie could not be found')

            event = Event(name=data['name'], 
                          description=data['description'], 
                          categorie_id=categorie.id,
                          public=data['public']
                          )
            
            try:
                    json_room_list = []
                    for room_id in rooms:
                        room_in_event = RoomInEvent(room_id=room_id, event_id=event.id)
                        room_in_event.add_to_db()

                        room = Room.find_by_id(id=room_in_event.room_id)
                        json_room=room.json()
                        json_room_list.append(json_room)
                        
                    json_prestataire_list=[]
                    for prestataire_id in prestataires:
                        prestataire_in_event = PrestataireInEvent(prestataire_id=prestataire_id, event_id=event.id)
                        prestataire_in_event.add_to_db()

                        prestataire = Prestataire.find_by_id(id=prestataire_in_event.prestataire_id)
                        json_prestataire= prestataire.json()
                        json_prestataire_list.append(json_prestataire)

                    event.add_to_db()
                    
                    event_json = event.json(prestataire=json_prestataire_list, room=json_room_list)
 
            except Exception as e:
                    logging.error(e) 
                    abort(422, 'An error occurred creating the event')

            else:
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
                categorie = Categorie.find_by_id(id=event.categorie_id) 
                json_categorie = categorie.json()

                prestataire_in_event_list = PrestataireInEvent.find_by_event_id(event_id=event.id)
                json_prestataire_list = []

                if prestataire_in_event_list:
                    for prestataire_id in prestataire_in_event_list:
                        prestataire_in_event = PrestataireInEvent(prestataire_id=prestataire_id, event_id=event.id)
                        prestataire_in_event.add_to_db()

                        prestataire = Prestataire.find_by_id(id=prestataire_in_event.prestataire_id)
                        json_prestataire= prestataire.json()
                        json_prestataire_list.append(json_prestataire)
                else:
                    json_prestataire_list={}
 
                room_in_event_list = RoomInEvent.find_by_event_id(event_id=event.id)
                json_room_list = []

                if room_in_event_list:
                    for room_id in room_in_event_list:
                        room_in_event = RoomInEvent(room_id=room_id, event_id=event.id)
                        room_in_event.add_to_db()

                        room = Room.find_by_id(id=room_in_event.room_id)
                        json_room=room.json()
                        json_room_list.append(json_room)

                else:
                    json_room_list={}

                categorie = Categorie.find_by_id(id=event.categorie_id) 
                json_categorie = categorie.json()

                json_event = event.json(prestataire=json_prestataire_list, categorie=json_categorie, room=json_room_list)
            
            else:
                event_list=Event.find_all()
                json_event = Event.all_json(event_list=event_list)

            if not event:
                abort(405, 'Event could not be found')
            
            response = current_app.response_class(response=json.dumps(json_event), status=200, mimetype='application/json')
            return response 

    @token_required
    def delete(self, user):
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

            prestataire_in_events = PrestataireInEvent.find_by_event_id(event_id=event.id)
            for prestataire_in_event in prestataire_in_events:
                try:
                    prestataire_in_event.remove_from_db()
                except Exception as e:
                    logging.error(e) 
                    abort(400, 'Cannot remove prestataire from event')

            room_in_events = RoomInEvent.find_by_event_id(event_id=event.id)
            for room_in_event in room_in_events:
                try:
                    room_in_event.remove_from_db()
                except Exception as e:
                    logging.error(e) 
                    abort(400, 'Cannot remove room from event')

            try:
                event.remove_from_db()

            except:
                logging.error(e)
                abort(422, 'An error occurred deleting the event')
            else:
                response = current_app.response_class(response=json.dumps(dict(message='event deleted')), status=204, mimetype='application/json')
 
                return response
            

    @token_required
    def patch(self, user):
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
        parser.add_argument(**vars(self.__optional__(self.categorie_id)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)  
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            if 'public' in data:
                if user.level != ADMIN_LEVEL:
                    data.pop('public')



            #On teste si les room et les prestataire a patcher existe
            rooms=[]
            if data['room_id']:
                for room_id in data['room_id']:
                        room = Room.find_by_id(id=room_id)
                        if not room:
                            abort(405, 'Room could not be found')
                        else:
                            rooms.append(room.id) 

            if data['prestataire_id']:
                prestataires=[]
                for prestataire_id in data['prestataire_id']:
                        prestataire = Prestataire.find_by_id(id=prestataire_id)
                        if not prestataire:
                            abort(405, 'Prestataire could not be found')
                        else:
                            prestataires.append(prestataire.id) 
                            
            #On teste si l'évènement a patcher existe
            event = Event.find_by_id(id=data['id'])
            if not event:
                    abort(404, dict(message='Event could not be found'))


            #On ajoute les nouelle room et les nouveaux prestataire dans l'event
            json_room_list=[]
            for room_id in rooms:
                room_in_event = RoomInEvent.find_by_room_event_id(event_id=event.id, room_id=room_id)
                if not room_in_event:
                    room_in_event = RoomInEvent(room_id=room_id, event_id=event.id)
                    room_in_event.add_to_db()
                    
                room = Room.find_by_id(id=room_in_event.room_id)
                json_room=room.json()
                json_room_list.append(json_room)

            json_prestataire_list=[]
            for prestataire_id in prestataires:
                prestataire_in_event = PrestataireInEvent.find_by_prestataire_event_id(event_id=event.id, prestataire_id=prestataire_id)
                if not prestataire_in_event:
                    prestataire_in_event = PrestataireInEvent(prestataire_id=prestataire_id, event_id=event.id)
                    prestataire_in_event.add_to_db()
                    
                prestataire = Prestataire.find_by_id(id=prestataire_in_event.prestataire_id)
                json_prestataire= prestataire.json()
                json_prestataire_list.append(json_prestataire)

            #On détruit toutes les lien room et tous les lien prestataires qui ne font plus parti de l'event
            all_current_room = RoomInEvent.find_by_event_id(event_id=event.id)
            all_current_prestataire = PrestataireInEvent.find_by_event_id(event_id=event.id)

            for r in all_current_room:
                if r.id not in rooms:
                    r.remove_from_db()

            for p in all_current_prestataire:
                if p.id not in rooms:
                    p.remove_from_db()


            if data['categorie_id']:
                    categorie = Categorie.find_by_id(id=data['categorie_id'])
                    if not categorie:
                        abort(405, 'Categorie could not be found')

            del data["prestataire_id"]
            del data["room_id"]

            keys_to_patch = dict()
            for key in data.keys():
                    if data[key] and data[key] != '': 
                        keys_to_patch[key] = data[key]
 
            try:
                event.patch_in_db(keys_to_patch)
                    
            except Exception as e:
                    logging.error(e)   
                    abort(405, dict(message='Cannot update vent'))

            else:
                event_json = event.json(prestataire=json_prestataire_list, room=json_room_list)
                response = current_app.response_class(response=json.dumps(event_json), status=201, mimetype='application/json')
                return response 