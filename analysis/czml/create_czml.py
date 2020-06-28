import json
from analysis.models import session, Node


START_TIME = '2012-03-15T10:00:00Z'
END_TIME = '2012-03-16T10:00:00Z'


def create_czml():
    return [{
        'id': 'document',
        'name': 'test',
        'version': '1.0',
        # 'clock': {
        #     'interval': f'{START_TIME}/{END_TIME}',
        #     'currentTime': START_TIME,
        #     'multiplier': 60,
        #     'range': 'LOOP_STOP',
        #     'step': 'SYSTEM_CLOCK_MULTIPLIER'
        # },
    }]


def create_train_czml():
    czml = create_czml()
    nodes = session.query(Node)
    for node in nodes:
        if not node.st1 or not node.st2:
            continue
        st1 = node.st1
        st2 = node.st2
        print(st1.name, st1.lat, st1.lng)
        print(st2.name, st2.lat, st2.lng)
        print()
        czml.append({
            'id': str(node.id),
            'name': str(node.id),
            'polyline': {
                'positions': {
                    'cartographicDegrees': [
                        st1.lng, st1.lat, 0,
                        st2.lng, st2.lat, 0,
                    ],
                },
                'material': {
                    'solidColor': {
                        'color': {
                            'rgba': [128, 0, 0, 255],
                        },
                    },
                },
                'width': 1.0,
            },
        })
    return czml


with open('./public/test.czml', 'w') as f:
    data = create_train_czml()
    f.write(json.dumps(data, sort_keys=True, indent=2))
