# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from resources.verification import token_required
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.event import Event, EventUserSubscription


class EventSubscription(Resource):

    """ Product basket' endpoint. """

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    user_id = Namespace(name='user_id', default=0, dest="user_id", action='store', type=int)
    event_id = Namespace(name='event_id', default=0, dest="event_id", action='store', type=int)


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
            Post an EventUserSubscription
            :type user: User 
            :params:    event_id: event id of the user
                        user_id: user id of the user

            :return: ProductBasket json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.event_id)))

        try:
            data = parser.parse_args()
            del parser
 
        except Exception as e:
            logging.error(e) 
            abort(400, 'Missing required parameter in the JSON body')
         
        else:
            event = Event.find_by_id(id=data['event_id'])
            if not event:
                abort(405, 'Event could not be found')

            event_list_user = EventUserSubscription(user_id=user.id, event_id=data['event_id'])
 
            try:
                event_list_user.add_to_db()
                event_list_user_json = event_list_user.json()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred subscribint the user to the event')
               
            else:
                response = current_app.response_class(response=json.dumps(event_list_user_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def get(self, user):
        """
            Get an Prestataire
            :params:    id: id of the Prestataire to get

            :return: Product json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.id)))

        data = parser.parse_args()
        del parser

        if data['id']: 
            event = EventUserSubscription.find_by_id(id=data['id'])
            if not event:
                abort(405, 'Event could not be found')

            json_event_user = event.json()

        else:
            event_list = EventUserSubscription.find_all()
            if not event_list:
                abort(405, 'Event list could not be found')

            json_event_user = EventUserSubscription.all_json(prestataire_list=event_list)

        response = current_app.response_class(response=json.dumps(json_event_user), status=200,
                                                      mimetype='application/json')
        return response


    @token_required
    def delete(self, user): 
        """
            Patch an ProductBasket
            :type user: User
            :params:    id: id of the product basket to delete
            
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
            try:
                event_user = EventUserSubscription.find_by_id(id=data['id'])
                if not event_user:
                    abort(405, 'Event user could not be found')

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the user event subscription')

            else:
                response = current_app.response_class(response=json.dumps(dict(message='event user deleted')), status=201,
                                                    mimetype='application/json')
                return response