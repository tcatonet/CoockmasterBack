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
from utils.global_config import CLOSE, PRIVATE

from models.event import Event, EventUserSubscription, RoomInEvent


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

            if event.access == CLOSE:
                abort(400, 'The subscriptions for this event are closed')

            event_room_list = RoomInEvent.find_by_event_id(event_id=event.id)
            
            room_affect_to_user = None
            remaining_capacity = 0
            for event_room in event_room_list:
                remaining_capacity = event_room.max_capacity-event_room.current_capacity
                if remaining_capacity > 0:
                    room_affect_to_user=event_room
            
            if room_affect_to_user: 
                room_affect_to_user
                remaining_capacity -=1
                room_affect_to_user.patch_in_db({"current_capacity": event_room.current_capacity+1})

            else:
                abort(400, 'The subscriptions for this event are closed '+str(event_room_list))

            if not remaining_capacity:
                event.patch_in_db({"access": CLOSE})

            event_subscription = EventUserSubscription(user_id=user.id, event_id=data['event_id'], room_id=room_affect_to_user.room_id)

            try:
                event_subscription.add_to_db()
                event_subscription_json = event_subscription.json()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred subscribing a user to an event')
               
            else:
                response = current_app.response_class(response=json.dumps(event_subscription_json), status=201,
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
            event_subscription = EventUserSubscription.find_by_id(id=data['id'])
            if not event_subscription:
                abort(405, 'Event subscription could not be found') 

            event_subscription_json = event_subscription.json()

        else:
            event_list = EventUserSubscription.find_by_user_id(user_id=user.id)
            event_subscription_json = EventUserSubscription.all_json(event_list=event_list)

        response = current_app.response_class(response=json.dumps(event_subscription_json), status=200,
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
                event_subscription = EventUserSubscription.find_by_id(id=data['id'])
                if not event_subscription:
                    abort(405, 'Event subscription could not be found')

                room_in_event = RoomInEvent.find_by_event_id_room_id(event_id=event_subscription.event_id, room_id=event_subscription.room_id)
                room_in_event.patch_in_db({'current_capacity': room_in_event.current_capacity-1})
                event_subscription.remove_from_db()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred deleting the user event subscription')

            else:
                response = current_app.response_class(response=json.dumps({'message':'Event subscription deleted'}), status=201,
                                                    mimetype='application/json')
                return response