import json
from analysis.models import session, Node, Station, Railway, IS_SUBWAY, IS_DISPLAYED


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


def station(st):
    is_subway = st.railway.operator_id in IS_SUBWAY
    delta = 0.0005
    if is_subway:
        height = -100
        color = [255, 0, 0, 255]
    else:
        height = 100
        color = [0, 255, 0, 255]

    positions = [
        st.lng + delta, st.lat + delta, height,
        st.lng + delta, st.lat - delta, height,
        st.lng - delta, st.lat - delta, height,
        st.lng - delta, st.lat + delta, height,
    ]

    name = f'{st.name} / {st.railway.name}'
    return {
        'id': st.id,
        'name': name,
        'polygon': {
            'positions': {
                'cartographicDegrees': positions,
            },
            'material': {
                'solidColor': {
                    'color': {
                        'rgba': color
                    },
                },
            },
            'extrudedHeight': height,
            'height': height * 2,
            'perPositionHeight': False,
        },
    }


def rail(node):
    pass


def create_train_czml():
    czml = create_czml()
    nodes = list(
        session.query(Node).join(Node.st1, Station.railway)
        .filter(Railway.operator_id.in_(IS_DISPLAYED))
    )
    ops = set()
    print('queried')
    for node in nodes:
        if not node.st1 or not node.st2:
            continue
        st1 = node.st1
        st2 = node.st2
        ops.add(st1.railway.operator_id)
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
        czml.append(station(st1))
    return czml


with open('./public/test.czml', 'w') as f:
    data = create_train_czml()
    f.write(json.dumps(data, sort_keys=True, indent=2))
