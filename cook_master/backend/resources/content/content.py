# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.content import Content, ContentAggregate
from resources.verification import token_required, admin_token_required


class ContentText(Resource): 

    """ Product endpoint. """  
  
    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    content_aggregate_id = Namespace(name='content_aggregate_id', default=0, dest="content_aggregate_id", action='store', type=int)
    title = Namespace(name='title', default='', dest="title", action='store', type=str)
    content = Namespace(name='content', default='', dest="content", action='store', type=str)

  
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
            Get an event categorie
            :params:    room_mandatory: room_mandatory of the event categorie to create
                        prestataire_mandatory: prestataire_mandatory of the event categorie to create

            :return: Product json data. 
            :rtype: application/json.
        """    
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.title)))
        parser.add_argument(**vars(self.__required__(self.content)))
        parser.add_argument(**vars(self.__required__(self.content_aggregate_id)))

        try:
            data = parser.parse_args()
            del parser
            if data['title'] == '':
                abort(400, 'invalid title')
            if data['content'] == '':
                abort(400, 'invalid content')

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            content_aggregate = ContentAggregate.find_by_id(id=data['content_aggregate_id'])
            if not content_aggregate:
                abort(405, 'content aggregate could not be found')

            existing_content_list = Content.find_by_aggregate_content_id(content_aggregate_id=data['content_aggregate_id'])

            content = Content(title=data['title'], content=data['content'],content_aggregate_id=data['content_aggregate_id'], rank=len(existing_content_list))

            try:
                content.add_to_db()
                content_json = content.json()

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the content')
                
            else:
                response = current_app.response_class(response=json.dumps(content_json), status=201,
                                                    mimetype='application/json')
                return response


    @token_required
    def get(self, user):
        """
            Get an Product
            :params:    name: name of the product to get

            :return: Product json data.
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__optional__(self.id)))

        try:
            data = parser.parse_args()
            del parser
        
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if data['id']: 

                content = Content.find_by_id(id=data['id'])
                if not content:
                    abort(405, 'Content could not be found')

                json_content= content.json()

            else:
                json_content = Content.find_all()
                json_content = Content.all_json(content_list=json_content)

            response = current_app.response_class(response=json.dumps(json_content), status=200,
                                                        mimetype='application/json')
            return response


    @admin_token_required
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
            content = Content.find_by_id(id=data['id'])
            if not content:
                abort(405, 'Content could not be found')

            try: 
                content.remove_from_db()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred deteting the event content')

            else:
                response = current_app.response_class(response=json.dumps({'message':'content deleted'}), status=203, mimetype='application/json')
                return response



    @admin_token_required
    def patch(self, user): 
        """
            Patch a Product
            :params:    name: name of the product to patch
                        description: description of the product to patch
                        stock: stock of the product to patch
                        prix: prix of the product to patch

            :return: Product json data 
            :rtype: application/json.
        """
        parser = reqparse.RequestParser()
        parser.add_argument(**vars(self.__required__(self.id)))
        parser.add_argument(**vars(self.__optional__(self.title)))
        parser.add_argument(**vars(self.__optional__(self.content)))
        parser.add_argument(**vars(self.__optional__(self.content_aggregate_id)))

        try: 
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e) 
            abort(400, dict(message='Missing required parameter in the JSON body'))

        else:
            if data['title']:
                if data['title'] == '':
                    abort(400, 'invalid title')

            if data['content']:
                if data['content'] == '':
                    abort(400, 'invalid content')

            if data['content_aggregate_id']:
                content_aggregate_id = ContentAggregate.find_by_id(id=data['content_aggregate_id'])
                if not content_aggregate_id:
                    abort(405, 'content could not be found')

            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '': 
                    keys_to_patch[key] = data[key]

            content = Content.find_by_id(id=data['id'])
            if not content:
                abort(404, dict(message='Content could not be found'))

            try:
                content.patch_in_db(keys_to_patch)
                json_content= content.json()

            except Exception as e:
                logging.error(e) 
                abort(422, 'An error occurred patching the content')
 
            else:
                response = current_app.response_class(response=json.dumps(json_content), status=201, mimetype='application/json')
                return response