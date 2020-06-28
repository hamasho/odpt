from sqlalchemy import Column, Integer, String, Float, ForeignKey
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


class Station(Base):
    id = Column(String, primary_key=True)
    railway_id = Column(String, ForeignKey('railway.id'), nullable=False)
    name = Column(String, nullable=False)
    name_ja = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)


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
