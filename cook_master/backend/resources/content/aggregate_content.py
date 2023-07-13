# Thomas Catonet
# Version 1.0
# -*- coding: utf-8 -*-

import json
import copy
import logging

from argparse import Namespace
from flask import abort, current_app
from flask_restful import Resource, reqparse

from models.content import CategorieContent, ContentAggregate, Content
from resources.verification import token_required, admin_token_required


class AggregateContent(Resource): 

    """ Product endpoint. """  

    id = Namespace(name='id', default=0, dest="id", action='store', type=int)
    page = Namespace(name='page', default=0, dest="page", action='store', type=int)
    categorie_id = Namespace(name='categorie_id', default=0, dest="categorie_id", action='store', type=int)
    title = Namespace(name='title', default='', dest="title", action='store', type=str)
    description = Namespace(name='description', default='', dest="description", action='store', type=str)

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
        parser.add_argument(**vars(self.__required__(self.description)))
        parser.add_argument(**vars(self.__required__(self.categorie_id)))

        try:
            data = parser.parse_args()
            del parser

        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
         
        else:
            if data['title'] == '':
                abort(400, 'invalid title')
            if data['description'] == '':
                abort(400, 'invalid description')
                
            categorie = CategorieContent.find_by_id(id=data['categorie_id'])
            if not categorie:
                abort(405, 'Categorie could not be found')

            content_aggregate = ContentAggregate(title=data['title'], description=data['description'], categorie_id=data['categorie_id'])

            try:
                content_aggregate.add_to_db()
                
                existing_content_list = Content.find_by_aggregate_content_id(content_aggregate_id=content_aggregate.id)
                json_existing_content_list = Content.all_json(content_list=existing_content_list)
                categorie = CategorieContent.find_by_id(id=content_aggregate.categorie_id)
                json_categorie=categorie.json()
                json_content_aggregate= content_aggregate.json(json_categorie=json_categorie, json_content_list=json_existing_content_list)

            except Exception as e:
                logging.error(e)
                abort(422, 'An error occurred creating the content')
                
            else:
                response = current_app.response_class(response=json.dumps(json_content_aggregate), status=201,
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
        parser.add_argument(**vars(self.__optional__(self.page)))

        try:
            data = parser.parse_args()
            del parser
        
        except Exception as e:
            logging.error(e)
            abort(400, 'Missing required parameter in the JSON body')
        
        else:
            if data['id']: 

                content_aggregate = ContentAggregate.find_by_id(id=data['id'])
                if not content_aggregate:
                    abort(405, 'Content could not be found')
 
                content_aggregate.add_to_db()
                existing_content_list = Content.find_by_aggregate_content_id(content_aggregate_id=content_aggregate.id)
                json_existing_content_list = Content.all_json(content_list=existing_content_list)
                categorie = CategorieContent.find_by_id(id=content_aggregate.categorie_id)
                json_categorie=categorie.json()
                json_content_aggregate= content_aggregate.json(json_categorie=json_categorie, json_content_list=json_existing_content_list)

            else:
                if not data['page']:                 
                    data['page']=1

                content_aggregate_list = ContentAggregate.find_all(page=data['page'])
                json_content_aggregate = ContentAggregate.all_json(content_aggregate_list=content_aggregate_list)

            response = current_app.response_class(response=json.dumps(json_content_aggregate), status=200,
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
            content_aggregate = ContentAggregate.find_by_id(id=data['id'])
            if not content_aggregate:
                abort(405, 'Content could not be found')

            try: 
                content_aggregate.remove_from_db()

            except Exception as e:
               logging.error(e)
               abort(422, 'An error occurred deteting the event content aggregate')

            else:
                response = current_app.response_class(response=json.dumps({'message':'content aggregate deleted'}), status=203, mimetype='application/json')
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
        parser.add_argument(**vars(self.__optional__(self.description)))
        parser.add_argument(**vars(self.__optional__(self.categorie_id)))

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

            if data['description']:
                if data['description'] == '':
                    abort(400, 'invalid description')

            if data['categorie_id']:
                categorie = CategorieContent.find_by_id(id=data['categorie_id'])
                if not categorie:
                    abort(405, 'Categorie could not be found')

            keys_to_patch = dict()
            for key in data.keys():
                if data[key] and data[key] != '': 
                    keys_to_patch[key] = data[key]

            content_aggregate = ContentAggregate.find_by_id(id=data['id'])
            if not content_aggregate:
                abort(404, dict(message='Aggregate content could not be found'))

            try:
                content_aggregate.patch_in_db(keys_to_patch)

                existing_content_list = Content.find_by_aggregate_content_id(content_aggregate_id=content_aggregate.id)
                json_existing_content_list = Content.all_json(content_list=existing_content_list)
                categorie = CategorieContent.find_by_id(id=content_aggregate.categorie_id)
                json_categorie=categorie.json()
                json_content_aggregate= content_aggregate.json(json_categorie=json_categorie, json_content_list=json_existing_content_list)


            except Exception as e:
                logging.error(e) 
                abort(422, 'An error occurred patching the aggregate content')

            else:
                response = current_app.response_class(response=json.dumps(json_content_aggregate), status=200, mimetype='application/json')
                return response