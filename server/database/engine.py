from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")  # or other relevant config var
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`


engine = create_engine(db_url)

Base = declarative_base()

class Class_(Base):
    __tablename__ = 'class'

    id = Column(Integer, primary_key=True)
    class_name = Column(String(255))
    class_description = Column(Text)

class Background(Base):
    __tablename__ = 'background'

    id = Column(Integer, primary_key=True)
    background_name = Column(String(255))
    background_description = Column(Text)

class Race(Base):
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True)
    race_name = Column(String(255))
    race_description = Column(Text)

    sub_race = relationship('SubRace', back_populates='race')

class SubRace(Base):
    __tablename__ = 'sub_race'

    id = Column(Integer, primary_key=True)
    parent_race_id = Column(Integer, ForeignKey('race.id'))
    sub_race_name = Column(String(255))
    sub_race_description = Column(Text)

    race = relationship('Race', back_populates='sub_race')

class Actor(Base):
    __tablename__ = 'actor'

    id = Column(Integer, primary_key=True)
    first_name = Column(Text)
    middle_name = Column(Text)
    last_name = Column(Text)
    title = Column(Text)
    actor_age = Column(Integer)
    class_id = Column(Integer, ForeignKey('class.id'))
    class_ = relationship('Class_', foreign_keys=[class_id])
    actor_level = Column(Integer)
    background_id = Column(Integer, ForeignKey('background.id'))
    background = relationship('Background', foreign_keys=[background_id])
    job = Column(Text)
    actor_role = Column(Text)
    race_id = Column(Integer, ForeignKey('race.id'))
    race = relationship('Race', foreign_keys=[race_id])
    sub_race_id = Column(Integer, ForeignKey('sub_race.id'))
    sub_race = relationship('SubRace', foreign_keys=[sub_race_id])
    alignment = Column(String(2))
    strength = Column(Integer)
    dexterity = Column(Integer)
    constitution = Column(Integer)
    intelligence = Column(Integer)
    wisdom = Column(Integer)
    charisma = Column(Integer)
    ideal = Column(Text)
    bond = Column(Text)
    flaw = Column(Text)
    appearance = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    notes = Column(Text)

class Skills(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    skill_name = Column(String(255))
    skill_description = Column(Text)
    skill_trait = Column(String(255))

class ActorToSkills(Base):
    __tablename__ = 'actor_to_skills'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    skill_level = Column(Integer)


class Faction(Base):
    __tablename__ = 'faction'

    id = Column(Integer, primary_key=True)
    faction_name = Column(String(255))
    faction_description = Column(Text)
    goals = Column(Text)
    faction_values = Column(Text)
    faction_income_sources = Column(Text)
    faction_expenses = Column(Text)


class FactionAOnBRelations(Base):
    __tablename__ = 'faction_a_on_b_relations'

    id = Column(Integer, primary_key=True)
    faction_a_id = Column(Integer, ForeignKey('faction.id'))
    faction_b_id = Column(Integer, ForeignKey('faction.id'))
    overall = Column(Text)
    economically = Column(Text)
    politically = Column(Text)
    opinion = Column(Text)

    faction_a = relationship('Faction', foreign_keys=[faction_a_id])
    faction_b = relationship('Faction', foreign_keys=[faction_b_id])


class FactionMembers(Base):
    __tablename__ = 'faction_members'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    actor = relationship('Actor', foreign_keys=[actor_id])
    faction_id = Column(Integer, ForeignKey('faction.id'))
    faction = relationship('Faction', foreign_keys=[faction_id])
    actor_role = Column(String(255))
    relative_power = Column(Integer)


class Location(Base):
    __tablename__ = 'location_'

    id = Column(Integer, primary_key=True)
    location_name = Column(String(255))
    location_type = Column(String(255))
    location_description = Column(Text)
    sights = Column(Text)
    smells = Column(Text)
    sounds = Column(Text)
    feels = Column(Text)
    tastes = Column(Text)
    coordinates = Column(String(255))


class LocationToFaction(Base):
    __tablename__ = 'location_to_faction'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location_.id'))
    faction_id = Column(Integer, ForeignKey('faction.id'))
    faction_presence = Column(Float)
    faction_power = Column(Float)
    notes = Column(Text)

    location = relationship('Location', foreign_keys=[location_id])
    faction = relationship('Faction', foreign_keys=[faction_id])


class LocationDungeon(Base):
    __tablename__ = 'location_dungeon'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location_.id'))
    dangers = Column(Text)
    traps = Column(Text)
    secrets = Column(Text)

    location = relationship('Location', foreign_keys=[location_id])

class LocationCity(Base):
    __tablename__ = 'location_city'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location_.id'))
    government = Column(Text)

    location = relationship('Location', foreign_keys=[location_id])

class LocationCityDistricts(Base):
    __tablename__ = 'location_city_districts'

    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('location_.id'))
    district_id = Column(Integer, ForeignKey('location_.id'))

    location = relationship('Location', foreign_keys=[location_id])
    district = relationship('Location', foreign_keys=[district_id])

class Resident(Base):
    __tablename__ = 'residents'

    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    location_id = Column(Integer, ForeignKey('location_.id'))

    actor = relationship('Actor', foreign_keys=[actor_id])
    location = relationship('Location', foreign_keys=[location_id])

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    event_name = Column(String(255))
    event_year = Column(Integer)
    event_description = Column(Text)

class HistoryActor(Base):
    __tablename__ = 'history_actor'

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('history.id'))
    actor_id = Column(Integer, ForeignKey('actor.id'))

    history = relationship('History', foreign_keys=[history_id])
    actor = relationship('Actor', foreign_keys=[actor_id])

class HistoryLocation(Base):
    __tablename__ = 'history_location'

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('history.id'))
    location_id = Column(Integer, ForeignKey('location_.id'))

    history = relationship('History', foreign_keys=[history_id])
    location = relationship('Location', foreign_keys=[location_id])

class HistoryFaction(Base):
    __tablename__ = 'history_faction'

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('history.id'))
    faction_id = Column(Integer, ForeignKey('faction.id'))

    history = relationship('History', foreign_keys=[history_id])
    faction = relationship('Faction', foreign_keys=[faction_id])

class Object_(Base):
    __tablename__ = 'object_'

    id = Column(Integer, primary_key=True)
    object_name = Column(String(255))
    object_description = Column(Text)
    object_value = Column(Integer)
    rarity = Column(String(255))

class HistoryObject(Base):
    __tablename__ = 'history_object'

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('history.id'))
    object_id = Column(Integer, ForeignKey('object_.id'))

    history = relationship('History', foreign_keys=[history_id])
    object = relationship('Object_', foreign_keys=[object_id])

class ObjectToOwner(Base):
    __tablename__ = 'object_to_owner'

    id = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('object_.id'))
    actor_id = Column(Integer, ForeignKey('actor.id'))

    object = relationship('Object_', foreign_keys=[object_id])
    actor = relationship('Actor', foreign_keys=[actor_id])

class WorldData(Base):
    __tablename__ = 'world_data'

    id = Column(Integer, primary_key=True)
    data_name = Column(String(255))
    data_description = Column(Text)

class HistoryWorldData(Base):
    __tablename__ = 'history_world_data'

    id = Column(Integer, primary_key=True)
    history_id = Column(Integer, ForeignKey('history.id'))
    world_data_id = Column(Integer, ForeignKey('world_data.id'))

    history = relationship('History', foreign_keys=[history_id])
    world_data = relationship('WorldData', foreign_keys=[world_data_id])