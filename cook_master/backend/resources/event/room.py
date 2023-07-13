# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging
import re
from datetime import datetime

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Room, RoomInEvent
from resources.verification import token_required, admin_token_required
from utils.validation import valid_postcode_regex


class CompanyRoom(Resource):

    """ Room endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    page = Namespace(name='page', default=0, dest="page", action='store', type=int)
    city = Namespace(name='city', default=0, dest="city", action='store', type=str)
    postcode = Namespace(name='postcode', default=0, dest="postcode", action='store', type=str)
    adress = Namespace(name='adress', default=0, dest="adress", action='store', type=str)
    capacity = Namespace(name='capacity', default=0, dest="capacity", action='store', type=int)
    date_start = Namespace(name='date_start', default=0, dest="date_start", action='store', type=str)
    date_end = Namespace(name='date_end', default=0, dest="date_end", action='store', type=str)

 
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
    
    
    @admin_token_required
    def post(self, user):
        """
            Post a room
            :params:    city: city of the room 
                        postcode: postcode of the room
                        adress: adress of the room

            :return: Room json data. 
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.city)))
        parser.add_argument(**vars(self.__required__(self.postcode)))
        parser.add_argument(**vars(self.__required__(self.adress)))
        parser.add_argument(**vars(self.__required__(self.capacity)))

        try:  
            data = parser.parse_args() 
            del parser

        except Exception as e: 
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if not re.match(valid_postcode_regex, data['postcode']):
                abort(400, 'invalid postcode')
            if not data['postcode']: 
                abort(400, 'postcode cannot be empty')
            if not data['city']:
                abort(400, 'city cannot be empty') 
            if not data['adress']:  
                abort(400, 'adress cannot be empty')
            if data['capacity'] < 0:  
                abort(400, 'capacity cannot be negative')
            try:
                room = Room(city=data['city'], postcode=data['postcode'], adress=data['adress'], capacity=data['capacity'])
                room.add_to_db()
                room_json = room.json()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the room')
            else:
            
                response = current_app.response_class(response=json.dumps(room_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def get(self, user):
        """
            Get an room
            :params:    id: id of the room to get

            :return: Room json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.page)))
        parser.add_argument(**vars(self.__optional__(self.date_start)))
        parser.add_argument(**vars(self.__optional__(self.date_end)))


        try: 
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
         
        else:
            if data['id']:   
                room = Room.find_by_id(id=data['id'])
                if not room:
                    abort(404, dict(message='Room could not be found'))
                try:
                    json_room = room.json()
                except Exception as e:
                    logging.error(e) 
                    abort(422, 'An error occurred getting the room')
            else:
                if not data['page']:
                    data['page']=1

                if data['date_start'] and data['date_end']:
                    data['date_start']=datetime.strptime(data['date_start'], '%Y-%m-%d %H').date()
                    data['date_end']=datetime.strptime(data['date_end'], '%Y-%m-%d %H').date()
                    room_list = Room.find_all_by_date(page=data['page'], date_start=data['date_start'], date_end=data['date_end']) 

                else:
                    room_list = Room.find_all(page=data['page']) 

                if not room_list:
                    abort(404, dict(message='Room list could not be found'))

                try: 
                    json_room = Room.all_json(room_list=room_list)
                except Exception as e:
                    logging.error(e) 
                    abort(422, 'An error occurred getting the room')

            #else:
            response = current_app.response_class(response=json.dumps(json_room), status=200,
                                                            mimetype='application/json')
            return response


    @admin_token_required
    def delete(self, user):
        """
            Delete a Room
            :params:    id: id of the Room to delete

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
            room = Room.find_by_id(id=data['id'])
            if not room:
                abort(405, 'Room could not be found')

            room_in_events = RoomInEvent.find_by_room_id(room_id=room.id)
            for room_in_event in room_in_events:
                try:  
                    room_in_event.remove_from_db()
                except Exception as e: 
                    logging.error(e) 
                    abort(400, 'Cannot remove room from event')

            try:
                room.remove_from_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the room')

        response = current_app.response_class(response=json.dumps(dict(message='room deleted')), status=204, mimetype='application/json')

        return response


    @admin_token_required
    def patch(self, user):
        """
            Patch a Room
            :params:    id: id of the Room to patch
                        city: city of the Room to patch
                        postcode: postcode of the Room to patch
                        adress: adress of the Room to patch

            :return: Room json data 
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.city)))
        parser.add_argument(**vars(self.__optional__(self.postcode)))
        parser.add_argument(**vars(self.__optional__(self.adress)))
        parser.add_argument(**vars(self.__optional__(self.capacity)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e) 
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            if not re.match(valid_postcode_regex, data['postcode']):
                abort(400, 'invalid postcode')

            if data['capacity'] < 0:  
                abort(400, 'capacity cannot be negative')

            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '': 
                    keys_to_patch[key] = data[key]

            room = Room.find_by_id(id=data['id'])

            if not room:
                abort(404, dict(message='Room could not be found'))
            try:
                room.patch_in_db(keys_to_patch)
            except Exception as e:
                logging.error(e) 
                abort(422, 'An error occurred patching the room')

            response = current_app.response_class(response=json.dumps(dict(message='room udpated')), status=204, mimetype='application/json')
            return response