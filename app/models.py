from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base


class RawImport(Base):
    __tablename__ = "raw_imports"

    id: Mapped[int] = mapped_column(primary_key=True)
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
    region = Column(String, nullable=True)
    capital = Column(Boolean, default=False, nullable=False)
    city = Column(String, nullable=True)
    harbor = Column(Boolean, nullable=True)
    victory_points = Column(Integer, nullable=True)
    import_date = Column(DateTime, server_default=func.now(), nullable=False)
    processed: Mapped[bool] = mapped_column(
        Boolean, server_default="FALSE", nullable=False
    )


class Player(Base):
    __tablename__ = "players"

    def to_dict(self):
        return {
            "id": self.id,
            "travian_player_id": self.travian_player_id,
            "player_name": self.player_name,
            "alliance_id": self.alliance_id,
        }

    id: Mapped[int] = mapped_column(primary_key=True)
    travian_player_id = Column(Integer, index=True)
    player_name = Column(String, nullable=False, index=True)
    alliance_id = Column(Integer, ForeignKey("alliances.id"), nullable=True)

    villages = relationship("Village", back_populates="player", lazy="select")
    history = relationship("DailyChange", back_populates="player", lazy="select")
    alliance = relationship("Alliance", back_populates="players", lazy="select")


class Alliance(Base):
    __tablename__ = "alliances"

    id: Mapped[int] = mapped_column(primary_key=True)
    travian_alliance_id = Column(Integer, index=True)
    alliance_tag = Column(String, nullable=True, index=True)
    players = relationship("Player", back_populates="alliance", lazy="select")


class Village(Base):
    __tablename__ = "villages"

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "village_name": self.village_name,
            "tribe": self.tribe,
            "player_id": self.player_id,
            "population": self.population,
        }

    id: Mapped[int] = mapped_column(primary_key=True)
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

    player = relationship("Player", back_populates="villages", lazy="select")
    history = relationship("DailyChange", back_populates="village", lazy="select")


class DailyChange(Base):
    __tablename__ = "daily_changes"

    id: Mapped[int] = mapped_column(primary_key=True)
    village_id = Column(Integer, ForeignKey("villages.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    population_delta = Column(Integer, nullable=False)
    victory_points = Column(Integer, nullable=True)

    village = relationship("Village", back_populates="history")
    player = relationship("Player", back_populates="history")
