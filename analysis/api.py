import json
from json.decoder import JSONDecodeError
import requests
import requests_cache
from config import CONFIG


requests_cache.install_cache('response')

DATA_TYPES = [
    'odpt:PassengerSurvey',
    'odpt:Station',
    # 'odpt:StationTimetable',
    'odpt:Railway',
    'odpt:Operator',
]


_token = CONFIG['API_ACCESS_TOKEN']
URLS = {
    'passenger_survey': (
        'https://api-tokyochallenge.odpt.org/api/v4/'
        'odpt:PassengerSurvey?odpt:operator=odpt.Operator:TokyoMetro'
        '&acl:consumerKey={access_token}'
    ),
}


def to_json(res):
    try:
        return res.json()
    except JSONDecodeError:
        print('=== Response is not valid JSON ===')
        print(res.status_code)
        print(res.text)


def get_passenger():
    url = URLS['passenger_survey'].format(access_token=CONFIG['API_ACCESS_TOKEN'])
    res = requests.get(url)
    return res.json()


def dump_url(resource):
    url = (
        f'https://api-tokyochallenge.odpt.org/api/v4/{resource}.json'
        f'?acl:consumerKey={_token}'
    )
    return url


def download_all():
    result = {}
    for type in DATA_TYPES:
        url = dump_url(type)
        resp = requests.get(url)
        data = to_json(resp)
        result[type] = data
        print(type, len(data))
        __import__('pprint').pprint(data[0])
        with open(f'{CONFIG["PROJECT_DIR"]}/cache/{type}.json', 'w') as f:
            f.write(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
        print()
    return result
