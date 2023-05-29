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

URL = 'http://172.18.0.3:5000/'
TOKEN = ""
EMAIL = 'woyolan595@pixiil.com'
EMAIL2 = 'ofwyiqcq3z3@mail4k.com'
EMAIL3="rehoyi3174@carpetra.com"

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


class TestUserApplication:
    #pytest tests.py


    def test_create_user(self):
         x = requests.post("".join((URL,'register')), json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'})
         assert x.status_code == 201

    def test_create_user_with_wrong_email_format(self):
        x = requests.post("".join((URL,'register')), json={'email': 'testtest.com', 'password': 'bonjour', 'username': 'gérard'})
        assert x.status_code == 400


    def test_create_user_with_wrong_phone(self):
        x = requests.post("".join((URL,'register')), json={'email': EMAIL, 'phone': '0102', 'password': 'bonjour', 'username': 'gérard'})
        assert x.status_code == 400


    def test_create_user_with_an_existing_email(self):
        x = requests.post("".join((URL,'register')), json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'})
        assert x.status_code == 409


    def test_login_user_that_exist(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        assert x.status_code ==201


    def test_retrieve_user_that_exist(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']


        x = requests.get("".join((URL,'register')),
                            json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 200


    def test_update_user_that_exist(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.patch("".join((URL,'register')), 
                            json={'email': EMAIL2, 'password': 'bonjoure', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        assert x.status_code == 204


    def test_update_user_that_exist2(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL2, 'password': 'bonjoure'})
        token = x.json()['token']

        x = requests.patch("".join((URL,'register')), 
                            json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        assert x.status_code ==  204


    def test_update_user_with_wrong_email_format(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.patch("".join((URL,'register')), 
                            json={'email': 'testtest.com', 'password': 'bonjour', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        assert x.status_code == 400


    def test_update_user_with_wrong_phone(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.patch("".join((URL,'register')), 
                            json={'email': EMAIL, 'password': 'bonjour', 'phone': '0202', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        assert x.status_code == 400


    def test_update_user_with_an_existing_email(self):
        x = requests.post("".join((URL,'register')), json={'email': 'test@test2.com', 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': 'test@test2.com', 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.patch("".join((URL,'register')), 
                            json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                           )
        assert x.status_code == 409


    def test_delete_user_and_retrieve(self):
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.delete("".join((URL,'register')), 
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        assert x.status_code == 204


    def test_retrieve_user_who_was_destroy(self):
        x = requests.post("".join((URL,'register')), json={'email': 'aaa@aaa.fr', 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': 'aaa@aaa.fr', 'password': 'bonjour'})
        token = x.json()['token']

        x = requests.delete("".join((URL,'register')), 
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )

        x = requests.get("".join((URL,'register')),
                            json={'email': 'aaa@aaa.fr', 'password': 'bonjour', 'username': 'gérard'},
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                         )
        assert x.status_code == 401

    

    def test_retrieve_user_with_false_token(self):
        x = requests.get("".join((URL,'register')), 
                            json={'email': EMAIL}, 
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': "fhwfgwxgxxgxwgcwwg"}
                         )
        assert x.status_code == 401


    def test_retrieve_user_without_token(self):
        x = requests.get("".join((URL,'register')), 
                            json={'email': EMAIL}, 
                            headers={'Content-Type': 'Application/json'}
                         )
        assert x.status_code == 405


    def test_code_validation_email(self):
        x = requests.post("".join((URL,'register')), json={'email': EMAIL3, 'password': 'bonjour', 'username': 'gérard'})
        token = x.json()['refresh_token']
    
        y = requests.post("".join((URL,'mail')), json={
                                                        'code':100000, 
                                                        'x-access-tokens': token,                
                                                        'Content-Type': 'application/json;charset=utf-8',
                                                       })

        x = requests.delete("".join((URL,'register')), 
                            headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                            )
        assert y.status_code == 405