import json
from analysis.models import session, Node, Station, Railway, IS_SUBWAY, IS_DISPLAYED


START_TIME = '2012-03-15T10:00:00Z'
END_TIME = '2012-03-16T10:00:00Z'

HEIGHT = 100


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
        height = -HEIGHT
        color = [255, 0, 0, 255]
    else:
        height = HEIGHT
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
    st1 = node.st1
    st2 = node.st2
    name = f'{st1.name} <-> {st2.name}'
    is_subway = st1.railway.operator_id in IS_SUBWAY
    if is_subway:
        height = -HEIGHT
        color = [255, 192, 192, 128]
    else:
        height = HEIGHT
        color = [192, 255, 192, 128]

    result = {
        'id': str(node.id),
        'name': name,
        'polyline': {
            'positions': {
                'cartographicDegrees': [
                    st1.lng, st1.lat, height,
                    st2.lng, st2.lat, height,
                ],
            },
            'material': {
                'solidColor': {
                    'color': {
                        'rgba': color,
                    },
                },
            },
            'width': 3.0,
        },
    }
    return result


def create_train_czml():
    czml = create_czml()
    nodes = list(
        session.query(Node)
        .join(Node.st1, Station.railway)
        .filter(Railway.operator_id.in_(IS_DISPLAYED))
    )
    stations = {}
    print('queried')

    for node in nodes:
        st1 = node.st1
        st2 = node.st2
        if not st1 or not st2:
            continue

        czml.append(rail(node))
        stations[st1.id] = st1
        stations[st2.id] = st2

    for st in stations.values():
        czml.append(station(st))

    print('finished')

    return czml


with open('./public/test.czml', 'w') as f:
    data = create_train_czml()
    f.write(json.dumps(data, sort_keys=True, indent=2))
