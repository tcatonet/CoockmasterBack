from common import backend_url

test_user_login = {'name': 'get user', 'method': 'post',
                   'url': backend_url + 'login', 'data': dict(email='jean@mail.com', password="mdrsalut")}

test_logged_user = {'name': 'is user logged in ?', 'method': 'get',
                    'url': backend_url + 'login_required'}
