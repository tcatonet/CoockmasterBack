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

    def test_create_store(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_create_store'})
        assert x.status_code == 201

    def test_create_store_with_existing_name(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_create_store'})
        assert x.status_code == 422


    def test_create_product(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_create_product'})
        y = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'], 'name': 'name product test', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        assert x.status_code == 201

    def test_create_product_with_existing_name(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_create_product_with_existing_name'})
        x = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'],'name': 'name product test', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        assert x.status_code == 422

    def test_get_existing_product(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_get_existing_product'})
        p = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'], 'name': 'name product test2221', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        x = requests.get("".join((URL,'product')), json={'name': 'name product test2221'})
        assert x.status_code == 200

    def test_get_non_existing_product(self):
        x = requests.get("".join((URL,'product')), json={'name': '1'})
        assert x.status_code == 400

    def test_delete_product(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_delete_product'})
        x = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'], 'name': 'test_delete_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        x = requests.delete("".join((URL,'product')), json={'name': 'test_delete_product'})
        assert x.status_code == 204

    def test_delete_non_existing_product(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_delete_non_existing_product'})
        x = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'], 'name': 'test_delete_non_existing_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        x = requests.delete("".join((URL,'product')), json={'name': 'test_delete_non_existing_product'})
        x = requests.delete("".join((URL,'product')), json={'name': 'test_delete_non_existing_product'})
        assert x.status_code == 405


    def test_update_product(self):
        x = requests.post("".join((URL,'store')), json={'name': 'test_update_product'})
        x = requests.post("".join((URL,'product')), json={'store_id': x.json()['id'],'name': 'test_update_product', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        name = x.json()['name']
        y = requests.patch("".join((URL,'product')), json={'name': name})
        assert y.status_code == 204


    def test_get_product_store(self):
        a = requests.post("".join((URL,'store')), json={'name': 'test_get_product_store'})
        x = requests.post("".join((URL,'product')), json={'store_id': a.json()['id'], 'name': 'name product test88', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        x = requests.post("".join((URL,'product')), json={'store_id': a.json()['id'], 'name': 'name product test99', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        x = requests.get("".join((URL,'store')), json={'name': 'test_get_product_store'})
        assert x.status_code == 200





    def test_add_product_to_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL2, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL2, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_add_product_to_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99})

        
        name = p1.json()['name']
        p1 = requests.get("".join((URL,'product')), json={'name': name})
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert x.status_code == 201


    def test_get_all_product_from_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_get_all_product_from_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket2', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        p3 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_all_product_from_basket3', 'description': 'description product test', 'stock': 100, 'prix': 99.99})

        id1 = p1.json()['id']
        id2 = p2.json()['id']
        id3 = p3.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id3, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_delete_all_product_from_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL3, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL3, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_delete_all_product_from_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket1', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket2', 'description': 'description product test', 'stock': 100, 'prix': 99.99})
        p3 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_delete_all_product_from_basket3', 'description': 'description product test', 'stock': 100, 'prix': 99.99})

        id1 = p1.json()['id']
        id2 = p2.json()['id']
        id3 = p3.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id3, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.delete("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        assert x.status_code == 200



    def test_update_product_from_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL4, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL4, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_update_product_from_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_update_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.patch("".join((URL,'user_basket')), 
                                json={'id': id1, 'quantity':10}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_calculate_price_update_product_from_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL16, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL16, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_calculate_price_update_product_from_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_calculate_price_update_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 7})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.patch("".join((URL,'user_basket')), 
                                json={'id': id1, 'quantity':7}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        prix = x.json()['prix']

        assert prix == 49.0 and x.status_code == 201


    def test_delete_product_from_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL5, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL5, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_delete_product_from_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_delete_product_from_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id1 = x.json()['id']

        x = requests.delete("".join((URL,'user_basket')), 
                                json={'id': id1}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        x = requests.get("".join((URL,'basket')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_create_order(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL6, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL6, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_create_order'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_create_order', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_calculate_create_order(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL17, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL17, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_calculate_create_order'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_calculate_create_order', 'description': 'description product test', 'stock': 100, 'prix': 7})        
        id1 = p1.json()['id']

        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_calculate_create_order2', 'description': 'description product test', 'stock': 100, 'prix': 10})        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':7}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':3}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        prix = x.json()['prix']
        assert x.status_code == 200 and prix == 79
        

    def test_create_order_with_empty_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL15, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL15, 'password': 'bonjour'})
        token = x.json()['token']
        
        store = requests.post("".join((URL,'store')), json={'name': 'test_create_order_with_empty_basket'})
        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_create_order_with_empty_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 422


    def test_create_order_with_wrong_quantity(self):
        store = requests.post("".join((URL,'store')), json={'name': 'test_create_order_with_wrong_quantity'})
        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_create_order_with_wrong_quantity', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL13, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL13, 'password': 'bonjour'})
        token = x.json()['token']

        u2 = requests.post("".join((URL,'register')), json={'email': EMAIL14, 'password': 'bonjour', 'username': 'gérard'})
        y = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL14, 'password': 'bonjour'})
        token2 = x.json()['token']

        o = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':70}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        o = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':70}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token2}
                          )

        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token2}
                          )
        assert x.status_code == 422


    def test_get_order(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL7, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL7, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_get_order'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_order', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        a = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        id = a.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200
    

    def test_get_orders(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL8, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL8, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_get_orders'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_get_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': None}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        assert x.status_code == 200


    def test_cancel_orders(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL9, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL9, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_cancel_orders'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_cancel_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_cancel_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')),   
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        id = x.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        id = x.json()['id']

        x = requests.delete("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        

        assert x.status_code == 200


    def test_update_orders(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL10, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL10, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_update_orders'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_update_orders', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']
        p2 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_update_orders2', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id2 = p2.json()['id']

        x = requests.post("".join((URL,'user_basket')),   
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id2, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )


        x = requests.post("".join((URL,'user_order')), 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )

        id = x.json()['id']


        x = requests.get("".join((URL,'user_order')), 
                                json={'id': id}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        id = x.json()['id']


        x = requests.patch("".join((URL,'user_order')), 
                                json={'id': id, 'status': 'test'}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
        
        assert x.status_code == 200


    def test_add_product_to_basket(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL11, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL11, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_add_product_to_basket'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':2}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 201


    def test_add_product_to_basket_wicth_exceed_quantity(self):
        u1 = requests.post("".join((URL,'register')), json={'email': EMAIL12, 'password': 'bonjour', 'username': 'gérard'})
        x = requests.post("".join((URL,'login')), headers={'Content-Type': 'Application/json'}, json={'email': EMAIL12, 'password': 'bonjour'})
        token = x.json()['token']
        store = requests.post("".join((URL,'store')), json={'name': 'test_add_product_to_basket_wicth_exceed_quantity'})

        p1 = requests.post("".join((URL,'product')), json={'store_id': store.json()['id'], 'name': 'test_add_product_to_basket_wicth_exceed_quantity', 'description': 'description product test', 'stock': 100, 'prix': 99.99})        
        id1 = p1.json()['id']

        x = requests.post("".join((URL,'user_basket')), 
                                json={'product_id': id1, 'quantity':200}, 
                                headers={'Content-Type': 'Application/json', 'x-access-tokens': token}
                          )
    
        assert x.status_code == 422