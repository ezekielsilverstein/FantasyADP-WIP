from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerStandard(Base):
    __tablename__ = 'players_standard'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    name = Column(String)
    team = Column(String)
    posrank_str = Column(String)
    bye = Column(String)
    adp = Column(Float)
    best = Column(Integer)
    worst = Column(Integer)
    avg = Column(Float)
    stdev = Column(Float)
    position = Column(String)
    position_rank = Column(Integer)

class PlayerPPR(Base):
    __tablename__ = 'players_ppr'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    name = Column(String)
    team = Column(String)
    posrank_str = Column(String)
    bye = Column(String)
    adp = Column(Float)
    best = Column(Integer)
    worst = Column(Integer)
    avg = Column(Float)
    stdev = Column(Float)
    position = Column(String)
    position_rank = Column(Integer)

class PlayerHalfPPR(Base):
    __tablename__ = 'players_half_ppr'
    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    name = Column(String)
    team = Column(String)
    posrank_str = Column(String)
    bye = Column(String)
    adp = Column(Float)
    best = Column(Integer)
    worst = Column(Integer)
    avg = Column(Float)
    stdev = Column(Float)
    position = Column(String)
    position_rank = Column(Integer)
