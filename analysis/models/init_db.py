import datetime
from analysis.models.base import Base, engine, session
from analysis.models.stations import (
    Operator, Railway, Station, Node, Train, TrainTimetable,
    IS_DISPLAYED, MIN_TIME, MAX_TIME,
)
from analysis.api import download_all


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

all_data = download_all()
operators = all_data['odpt:Operator']
railways = all_data['odpt:Railway']
stations = all_data['odpt:Station']
timetables = all_data['odpt:TrainTimetable']


def init_operator():
    items = {}
    for item in operators:
        id = item['owl:sameAs']
        assert id not in items
        items[id] = Operator(
            id=id,
            name=item['odpt:operatorTitle']['en'],
            name_ja=item['dc:title'],
        )
    session.bulk_save_objects(items.values())


def get_nodes(orders):
    if len(orders) == 0 or len(orders) == 1:
        return []
    result = []
    for idx, order in enumerate(orders[:-1]):
        if order['odpt:index'] != idx + 1:
            raise ValueError('not in order')
        result.append(Node(
            st1_id=order['odpt:station'],
            st2_id=orders[idx + 1]['odpt:station'],
        ))
    return result


def init_railway():
    items = {}
    nodes = []
    for item in railways:
        id = item['owl:sameAs']
        assert id not in items
        items[id] = Railway(
            id=id,
            operator_id=item['odpt:operator'],
            name=item['odpt:railwayTitle']['en'],
            name_ja=item['dc:title'],
        )
        try:
            new_nodes = get_nodes(item['odpt:stationOrder'])
            nodes.extend(new_nodes)
        except ValueError:
            pass
    session.bulk_save_objects(items.values())
    session.bulk_save_objects(nodes)


def init_station():
    items = {}
    for item in stations:
        id = item['owl:sameAs']
        assert id not in items
        items[id] = Station(
            id=id,
            railway_id=item['odpt:railway'],
            name=item['odpt:stationTitle']['en'],
            name_ja=item['dc:title'],
            lat=item.get('geo:lat'),
            lng=item.get('geo:long'),
        )
    session.bulk_save_objects(items.values())


def init_timetable():
    trains = {}
    items = []
    for item in timetables:
        id = item['owl:sameAs']
        cal = item['odpt:calendar']
        if cal != 'odpt.Calendar:Weekday':
            continue
        # for DB speed optimization
        if item['odpt:operator'] not in IS_DISPLAYED:
            continue

        assert id not in trains
        trains[id] = Train(
            id=id,
            railway_id=item['odpt:railway'],
            name=item['odpt:trainNumber'],
            calendar=cal,
            type=item['odpt:trainType'],
        )

        for tt in item['odpt:trainTimetableObject']:
            time = tt.get('odpt:departureTime')
            st = tt.get('odpt:departureStation')
            if not time:
                time = tt.get('odpt:arrivalTime')
                st = tt.get('odpt:arrivalStation')
            if not time:
                continue

            h, m = time.split(':')
            time = datetime.time(int(h), int(m))
            if time < MIN_TIME or time > MAX_TIME:
                continue

            items.append(TrainTimetable(
                train_id=id,
                station_id=st,
                time=time,
            ))

    session.bulk_save_objects(items)
    session.bulk_save_objects(trains.values())


init_operator()
init_station()
init_railway()
init_timetable()
session.commit()
