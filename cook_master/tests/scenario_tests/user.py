from common import backend_url

test_get_user = {'name': 'get user', 'method': 'get',
                 'url': backend_url + 'register', 'data': dict(email='jean@mail.com')}

test_post_user = {'name': 'creating user', 'method': 'post',
                  'url': backend_url + 'register', 'data': dict(email='jean@mail.com', username='jean', password='mdrsalut')}

test_delete_user = {'name': 'deleting user', 'method': 'delete',
                    'url': backend_url + 'register', 'data': dict(email='jean@mail.com')}

test_patch_user = {'name': 'update user', 'method': 'patch',
                   'url': backend_url + 'register', 'data': dict(id=1, email='jean@mail.com', username='jeanjean')}
