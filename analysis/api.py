import json
import requests
import requests_cache
from config import CONFIG


requests_cache.install_cache('response')


URLS = {
    'passenger_survey': (
        'https://api-tokyochallenge.odpt.org/api/v4/'
        'odpt:PassengerSurvey?odpt:operator=odpt.Operator:TokyoMetro'
        '&acl:consumerKey={access_token}'
    ),
}

def get_passenger():
    url = URLS['passenger_survey'].format(access_token=CONFIG['API_ACCESS_TOKEN'])
    res = requests.get(url)
    return res.json()


with open('/tmp/test.json', 'w') as f:
    data = get_passenger()
    f.write(json.dumps(data, sort_keys=True, indent=2))
