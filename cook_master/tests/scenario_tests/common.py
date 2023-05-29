import json
import requests
from pprint import pprint, pformat

headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'close',
           'Content-Length': '16',
           'Content-Type': 'application/json'}

backend_url = "http://localhost:5000/"


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


def run_scenario(scenarios: list):
    print()
    for test in scenarios:
        print()
        print(f'{Colors.BLUE}{test["name"]}{Colors.ENDC}')
        print(f'\t{Colors.BLUE}Testing: {Colors.ENDC}{test["name"]}')
        print(f'\t{Colors.BLUE}Method: {Colors.ENDC}{test["method"]} ', end=' ')
        print(f'{Colors.BLUE}Testing {Colors.PURPLE}{test["url"]}{Colors.ENDC}')
        
        if 'data' not in test.keys():
            test['data'] = dict()
        print(f'\t{Colors.YELLOW}data {test["data"]}{Colors.ENDC}')

        if test['method'] == 'get':
            response = requests.get(test['url'], data=json.dumps(test['data']), headers=headers)
        elif test['method'] == 'post':
            response = requests.post(test['url'], data=json.dumps(test['data']), headers=headers)
        elif test['method'] == 'delete':
            response = requests.delete(test['url'], data=json.dumps(test['data']), headers=headers)
        elif test['method'] == 'patch':
            response = requests.patch(test['url'], data=json.dumps(test['data']), headers=headers)
        else:
            print('not supported')

        print(f"\tRESPONSE: {Colors.CYAN}", end=' ')
        print(f"\tCODE: {Colors.ENDC}", end=' ')
        print(response.status_code)

        if 200 <= response.status_code < 300:
            print(f'{Colors.GREEN}PASSED{Colors.ENDC}')
        else:
            print(f'{Colors.RED}KILLED{Colors.ENDC}')

        if not response.status_code:
            print(f'{Colors.RED}NO CODE{Colors.ENDC}')
        print(response.text)
