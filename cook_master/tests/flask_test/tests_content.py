import pprint
import logging
import datetime
import os
import pytest
import requests

class Colors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

URL = 'http://172.18.0.2:5000/'
TOKEN = ""
EMAIL_ADMIN = 'admin@admin.fr'

EMAIL = 'woyolan595@pixiil.com'
EMAIL2 = 'ofwyiqcq3z3@mail4k.com'
EMAIL3="rehoyi3174@carpetra.com"
EMAIL4="rehoyhi3174@carpetrah.com"
EMAIL5="rehoyhi3175@carpetrah.com"
EMAIL6="rehoyhi3176@carpetrah.com"
EMAIL7="rehoyhi3177@carpetrah.com"
EMAIL8="rehoyhi3178@carpetrah.com"
EMAIL9="rehoyhi3179@carpetrah.com"
EMAIL10="rehoyhi31710@carpetrah.com"
EMAIL11="rehoyhi31711@carpetrah.com"
EMAIL12="rehoyhi317122@carpetrah.com"
EMAIL13="rehoyhi317123@carpetrah.com"
EMAIL14="rehoyhi31714@carpetrah.com"
EMAIL15="rehoyhi31715@carpetrah.com"
EMAIL16="rehoyhi31716@carpetrah.com"
EMAIL17="rehoyhi31717@carpetrah.com"
EMAIL18="rehoyhi31718@carpetrah.com"
EMAIL19="rehoyhi31719@carpetrah.com"
EMAIL20="rehoyhi317120@carpetrah.com"
EMAIL21="rehoyhi317121@carpetrah.com"
EMAIL22="rehoyhi317121@carpetrah.com"
EMAIL23="rehoyhi31723@carpetrah.com"
EMAIL24="rehoyhi3171924@carpetrah.com"
EMAIL25="rehoyhi317125@carpetrah.com"
EMAIL26="rehoyhi317126@carpetrah.com"
EMAIL27="rehoyhi317127@carpetrah.com"


EMAIL28="rehoyhi31728@carpetrah.com"
EMAIL29="rehoyhi31729@carpetrah.com"
EMAIL30="rehoyhi317130@carpetrah.com"
EMAIL31="rehoyhi317131@carpetrah.com"
EMAIL32="rehoyhi317132@carpetrah.com"

class UnitLogger:
    def __init__(self, level=logging.ERROR):
        self.logger = logging.getLogger('Testing')

        # set log level
        self.logger.setLevel(level)

        # define file handler and set formatter
        time_now = datetime.datetime.now().strftime("day %m-%d time %H-%M-%S")
        if not os.path.exists('./logs/'):
            os.mkdir('./logs/')
            
        file_handler = logging.FileHandler(f'./logs/test-logs-{time_now}.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        
        # add file handler to logger
        self.logger.addHandler(file_handler)
        
    def log_something(self):
        # Logs
        self.logger.debug('A debug message')
        self.logger.info('An info message')
        self.logger.warning('Something is not right.')
        self.logger.error('A Major error has happened.')
        self.logger.critical('Fatal error. Cannot continue')

    @staticmethod
    def log_test_results(self, rv):
        print(f'{Colors.BLUE}status code{Colors.ENDC}')
        pprint.pprint(rv.status_code)
        print(f'{Colors.GREEN}response message{Colors.ENDC}')
        pprint.pprint(rv.data.decode())


class TestEcommerceApplication:
    #pytest tests.py
    

    def test_create_content_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_create_content_categorie'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201

    def test_create_existing_content_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_create_content_categorie'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 422



    def test_get_content_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_get_content_categorie'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.get("".join((URL,'/content/categorie')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        name = x.json()['name']

        assert x.status_code == 200 and name=='test_get_content_categorie'


    def test_delete_content_categorie(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_delete_categorie'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.delete("".join((URL,'/content/categorie')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 203


    def test_create_content_aggregate(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_create_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_create_content_aggregate', 'description': 'description test_create_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 201


    def test_get_content_aggregate(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_get_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_get_content_aggregate', 'description': 'content test_get_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']
        x = requests.get("".join((URL,'/content/aggregate')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        title = x.json()['title']


        assert x.status_code == 200 and title=='title test_get_content_aggregate'


    def test_delete_content_aggregate(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_delete_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_delete_content_aggregate', 'description': 'content test_delete_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.delete("".join((URL,'/content/aggregate')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 203


    def test_patch_content_aggregate(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_patch_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_patch_content_aggregate', 'description': 'content test_patch_content_aggregate'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']


        x = requests.patch("".join((URL,'/content/aggregate')), 
                                json={'id': id, 'title': 'title test_patch_content_aggregate 22'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        title = x.json()['title']

        assert x.status_code == 200 and title=='title test_patch_content_aggregate 22'


    def test_create_content(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_create_content', 'description': 'description test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content', 'content': 'description test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    

        assert x.status_code == 201


    def test_get_content(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_get_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_get_content', 'description': 'content test_get_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']
        x = requests.get("".join((URL,'/content/aggregate')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        title = x.json()['title']


        id = x.json()['id']

        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content', 'content': 'description test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content 111', 'content': 'description test_create_content 1111'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content 222', 'content': 'description test_create_content 222'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.get("".join((URL,'/content/aggregate')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200 and x.text == '{"id": 5, "title": "title test_get_content", "description": "content test_get_content", "categorie": {"id": 8, "name": "test_get_content"}, "contents": [{"id": 2, "rank": 0, "title": "title test_create_content", "content": "description test_create_content"}, {"id": 3, "rank": 1, "title": "title test_create_content 111", "content": "description test_create_content 1111"}, {"id": 4, "rank": 2, "title": "title test_create_content 222", "content": "description test_create_content 222"}]}'


    def test_delete_content(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_delete_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_delete_content', 'description': 'content test_delete_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content', 'content': 'description test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.delete("".join((URL,'/content')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 203


    def test_patch_content(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL_ADMIN, 'password': 'admin'})
        token = x.json()['token']

        x = requests.post("".join((URL,'/content/categorie')), 
                                json={'name': 'test_patch_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content/aggregate')), 
                                json={'categorie_id': id, 'title': 'title test_patch_content', 'description': 'content test_patch_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = x.json()['id']

        x = requests.post("".join((URL,'/content')), 
                                json={'content_aggregate_id': id, 'title': 'title test_create_content', 'content': 'description test_create_content'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        id = x.json()['id']

        x = requests.patch("".join((URL,'/content')), 
                                json={'id': id, 'title': 'title test_create_content500000', 'content': 'description -100000'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 201