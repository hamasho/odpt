import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Time
from sqlalchemy.orm import relationship
from .base import Base


class Operator(Base):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    name_ja = Column(String, nullable=False)


class Railway(Base):
    id = Column(String, primary_key=True)
    operator_id = Column(String, ForeignKey('operator.id'), nullable=False)
    name = Column(String, nullable=False)
    name_ja = Column(String, nullable=False)

    operator = relationship(Operator, lazy='joined')


class Station(Base):
    id = Column(String, primary_key=True)
    railway_id = Column(String, ForeignKey('railway.id'), nullable=False)
    name = Column(String, nullable=False)
    name_ja = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)

    railway = relationship(Railway, lazy='joined')


class Node(Base):
    id = Column(Integer, primary_key=True)
    st1_id = Column(String, ForeignKey('station.id'), nullable=False)
    st2_id = Column(String, ForeignKey('station.id'), nullable=False)

    st1 = relationship(
        Station,
        primaryjoin='(Node.st1_id == Station.id) & (Station.lat != None)',
        foreign_keys=[st1_id],
        lazy='joined',
    )
    st2 = relationship(
        Station,
        primaryjoin='(Node.st2_id == Station.id) & (Station.lat != None)',
        foreign_keys=[st2_id],
        lazy='joined',
    )


class Train(Base):
    id = Column(String, primary_key=True)
    railway_id = Column(String, ForeignKey('railway.id'), nullable=False)
    name = Column(String, nullable=False)
    calendar = Column(String, nullable=False)
    type = Column(String, nullable=False)

    railway = relationship(Railway, lazy='joined')
    timetables = relationship(
        'TrainTimetable', lazy='joined', backref='train',
        order_by='TrainTimetable.time',
    )


class TrainTimetable(Base):
    id = Column(Integer, primary_key=True)
    train_id = Column(String, ForeignKey('train.id'), nullable=False)
    station_id = Column(String, ForeignKey('station.id'), nullable=False)
    time = Column(Time, nullable=False)

    station = relationship(Station, lazy='joined', backref='timetables')


IS_RAILWAY_COMPANY = [
    'odpt.Operator:Aizu',
    'odpt.Operator:Chichibu',
    'odpt.Operator:Fujikyu',
    'odpt.Operator:HakoneTozan',
    'odpt.Operator:Hokuso',
    'odpt.Operator:IzuHakone',
    'odpt.Operator:Izukyu',
    'odpt.Operator:JR-Central',
    'odpt.Operator:JR-Shikoku',
    'odpt.Operator:JR-West',
    'odpt.Operator:KashimaRinkai',
    'odpt.Operator:Minatomirai',
    'odpt.Operator:SaitamaRailway',
    'odpt.Operator:Shibayama',
    'odpt.Operator:ShinKeisei',
    'odpt.Operator:Tobu',
    'odpt.Operator:Toei',
    'odpt.Operator:JR-East',
    'odpt.Operator:Keikyu',
    'odpt.Operator:Keio',
    'odpt.Operator:Keisei',
    'odpt.Operator:Odakyu',
    'odpt.Operator:Seibu',
    'odpt.Operator:TokyoMetro',
    'odpt.Operator:TokyoMonorail',
    'odpt.Operator:Hokuetsu',
    'odpt.Operator:Tokyu',
    'odpt.Operator:ToyoRapid',
    'odpt.Operator:Yagan',
    'odpt.Operator:Sotetsu',
    'odpt.Operator:Yurikamome',
    'odpt.Operator:TWR',
]

IS_DISPLAYED = [
    # 'odpt.Operator:JR-Central',
    # 'odpt.Operator:Minatomirai',
    # 'odpt.Operator:SaitamaRailway',
    # 'odpt.Operator:ShinKeisei',
    # 'odpt.Operator:Tobu',

    'odpt.Operator:Toei',
    'odpt.Operator:TokyoMetro',
    'odpt.Operator:JR-East',

    # 'odpt.Operator:Keikyu',
    # 'odpt.Operator:Keio',
    # 'odpt.Operator:Keisei',
    # 'odpt.Operator:Odakyu',
    # 'odpt.Operator:Seibu',

    # 'odpt.Operator:TokyoMonorail',
    # 'odpt.Operator:Tokyu',
    # 'odpt.Operator:ToyoRapid',
    # 'odpt.Operator:Yurikamome',
    # 'odpt.Operator:TWR',
]

IS_SUBWAY = [
    'odpt.Operator:Toei',
    'odpt.Operator:TokyoMetro',
]

MIN_TIME = datetime.time(10, 00)
MAX_TIME = datetime.time(13, 00)
