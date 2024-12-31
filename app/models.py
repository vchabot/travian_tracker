from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class RawImport(Base):
    __tablename__ = "raw_imports"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    tribe = Column(Integer, nullable=False)
    village_id = Column(Integer, nullable=False)
    village_name = Column(String, nullable=False)
    player_id = Column(Integer, nullable=False)
    player_name = Column(String, nullable=False)
    alliance_id = Column(Integer, nullable=True)
    alliance_tag = Column(String, nullable=True)
    population = Column(Integer, nullable=False)
    capital = Column(Boolean, default=False)
    city = Column(String, nullable=True)
    harbor = Column(Boolean, nullable=True)
    victory_points = Column(Integer, nullable=True)
    import_date = Column(DateTime, server_default=func.now())
    processed = Column(Boolean, default=False)

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    travian_player_id = Column(Integer, index=True)
    player_name = Column(String, nullable=False, index=True)
    alliance_id = Column(Integer, ForeignKey("alliances.id"), nullable=True)

    villages = relationship("Village", back_populates="player")
    history = relationship("DailyChange", back_populates="player")
    alliance = relationship("Alliance", back_populates="players")

class Alliance(Base):
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True, index=True)
    travian_alliance_id = Column(Integer, index=True)
    alliance_tag = Column(String, nullable=True, index=True)
    players = relationship("Player", back_populates="alliance")

class Village(Base):
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    travian_village_id = Column(Integer, index=True)
    village_name = Column(String, nullable=False)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    tribe = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    capital = Column(Boolean, default=False)
    city = Column(String, nullable=True)
    harbor = Column(Boolean, nullable=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    player = relationship("Player", back_populates="villages")
    history = relationship("DailyChange", back_populates="village")

class DailyChange(Base):
    __tablename__ = "daily_changes"

    id = Column(Integer, primary_key=True, index=True)
    village_id = Column(Integer, ForeignKey("villages.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    population_delta = Column(Integer, nullable=False)
    victory_points = Column(Integer, nullable=True)

    village = relationship("Village", back_populates="history")
    player = relationship("Player", back_populates="history")