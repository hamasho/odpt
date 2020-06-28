from analysis.models.base import Base, engine, Session
from analysis.models.stations import Operator, Railway, Station, Node
from analysis.api import download_all


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session()
# session.add(u)
# session.commit()

all_data = download_all()
operators = all_data['odpt:Operator']
railways = all_data['odpt:Railway']
stations = all_data['odpt:Station']


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
        __import__('pprint').pprint(order)
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


init_operator()
init_station()
init_railway()
session.commit()
