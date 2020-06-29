import json
import math
import datetime
from sqlalchemy.orm import joinedload
from analysis.models import (
    session, Node, Station, Railway, Train, TrainTimetable,
    IS_SUBWAY, IS_DISPLAYED,
)


START_HOUR = 11
END_HOUR = 12
START_T = datetime.time(START_HOUR, 0)
END_T = datetime.time(END_HOUR, 0)
TIME_FORMAT = '2020-06-29T{:02d}:{:02d}:00Z'
START_TIME = TIME_FORMAT.format(START_HOUR, 0)
END_TIME = TIME_FORMAT.format(END_HOUR, 0)

HEIGHT = 100
DELTA = 0.0005


def create_czml():
    return [{
        'id': 'document',
        'name': 'test',
        'version': '1.0',
        'clock': {
            'interval': f'{START_TIME}/{END_TIME}',
            'currentTime': START_TIME,
            'multiplier': 20,
            'range': 'LOOP_STOP',
            'step': 'SYSTEM_CLOCK_MULTIPLIER'
        },
    }]


def line2rect(p0, p1, thick, height):
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    ll = math.sqrt(dx*dx + dy*dy)
    dx /= ll
    dy /= ll
    px = 0.5 * thick * (-dy)
    py = 0.5 * thick * dx
    points = [
        x0 + px, y0 + py, height,
        x1 + px, y1 + py, height,
        x1 - px, y1 - py, height,
        x0 - px, y0 - py, height,
    ]
    return points


def station(st):
    is_subway = st.railway.operator_id in IS_SUBWAY
    if is_subway:
        height = -HEIGHT
        color = [255, 0, 0, 255]
    else:
        height = HEIGHT
        color = [0, 255, 0, 255]

    positions = [
        st.lng + DELTA, st.lat + DELTA, height,
        st.lng + DELTA, st.lat - DELTA, height,
        st.lng - DELTA, st.lat - DELTA, height,
        st.lng - DELTA, st.lat + DELTA, height,
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
        color = [255, 192, 192, 255]
    else:
        height = HEIGHT
        color = [192, 255, 192, 255]

    result = {
        'id': str(node.id),
        'name': name,
        'polygon': {
            'positions': {
                'cartographicDegrees': line2rect(
                    (st1.lng, st1.lat), (st2.lng, st2.lat), 0.0001, 1.4 * height,
                ),
            },
            'material': {
                'solidColor': {
                    'color': {
                        'rgba': color
                    },
                },
            },
            'extrudedHeight': 1.4 * height,
            'height': 1.6 * height,
            'perPositionHeight': False,
        },
    }
    return result


def time_diff(t1, t2):
    tt1 = datetime.datetime.combine(datetime.date.today(), t1)
    tt2 = datetime.datetime.combine(datetime.date.today(), t2)
    return (tt2 - tt1).seconds


def moving_train(train):
    is_subway = train.railway.operator_id in IS_SUBWAY
    if is_subway:
        height = -1.5 * HEIGHT
    else:
        height = 1.5 * HEIGHT

    tts = train.timetables
    if len(tts) <= 1:
        return []
    items = []
    for idx, tt in enumerate(tts[:-1]):
        tt2 = tts[idx + 1]
        if tt.time < START_T or tt2.time > END_T:
            continue

        start = TIME_FORMAT.format(tt.time.hour, tt.time.minute)
        end = TIME_FORMAT.format(tt2.time.hour, tt2.time.minute)
        id = f'{train.name} - {tt.time}-{tt2.time}'
        item = {
            'id': id,
            'name': id,
            'availability': f'{start}/{end}',
            "billboard" : {
                "eyeOffset" : {
                    "cartesian" : [0.0, 0.0, 0.0]
                },
                "horizontalOrigin" : "CENTER",
                "image" : "/train.png",
                "pixelOffset" : {
                    "cartesian2" : [0.0, 0.0]
                },
                "scale" : 0.09,
                "show" : True,
                "verticalOrigin" : "BOTTOM"
            },
            'position': {
                "interpolationAlgorithm" : "LINEAR",
                "interpolationDegree" : 1,
                'epoch': start,
                'cartographicDegrees': [
                    0,
                    tt.station.lng,
                    tt.station.lat,
                    height,
                    time_diff(tt.time, tt2.time),
                    tt2.station.lng,
                    tt2.station.lat,
                    height,
                ],
            }
        }
        items.append(item)
    return items


def create_stations_czml():
    print('start create_stations_czml')
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


def create_trains_czml():
    print('start create_trains_czml')
    czml = create_czml()
    trains = list(
        session.query(Train)
        .join(Train.timetables, Train.railway, TrainTimetable.station)
        .filter(Railway.operator_id.in_(IS_DISPLAYED))
        .options(joinedload(Train.timetables))
    )
    print('queried')
    for train in trains:
        czml.extend(moving_train(train))

    print('finished')
    return czml


with open('./public/stations.czml', 'w') as f:
    data = create_stations_czml()
    f.write(json.dumps(data, sort_keys=True, indent=2))

with open('./public/trains.czml', 'w') as f:
    data = create_trains_czml()
    f.write(json.dumps(data, sort_keys=True, indent=2))
