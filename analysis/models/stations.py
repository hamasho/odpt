from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base


class Operator(Base):
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    name_ja = Column(String, nullable=False)


class Railway(Base):
    id = Column(String, primary_key=True)
    operator_id = Column(String, ForeignKey('operator.id'), nullable=False)
    title = Column(String, nullable=False)
    title_ja = Column(String, nullable=False)


class Station(Base):
    id = Column(String, primary_key=True)
    railway_id = Column(String, ForeignKey('railway.id'), nullable=False)
    title = Column(String, nullable=False)
    title_ja = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)


class Node(Base):
    id = Column(Integer, primary_key=True)
    st1_id = Column(String, ForeignKey('station.id'), nullable=False)
    st2_id = Column(String, ForeignKey('station.id'), nullable=False)