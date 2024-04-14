from pydantic import BaseModel

description = """
Lorekeeper is a new app to manage the lore of your stories.


## History
Initially designed as a tool for a Dungeon Master, Lorekeeper aims to be the be all end all of lore managment.

## Components
Lorekeeper consists of a few elements.

- A PostreSQL sever to store the lore.
- A server (this file) to handle reqests to and from.
- A few seperate front ends
    1. a Foundry VTT module so users can access the lore from remotely
    2. a locally hosted webpage for exploring lore
    3. TODO: a desktop app for quickly adding lore to the database.

## Usage

The storyteller/DM can explore lore and add new entries to the database.

TODO: Entries can be linked in logical ways.

Operation should be as simple as Salesforce.

## Installation

**COMING SOON**
"""

tags_metadata = [
    {
        'name': 'Actors',
        'description': 'Actors are players/NPCs both are represented here.'
    },
    {
        'name': 'Faction',
        'description': 'Factions are the groups that vie for power.'
    },
    {
        'name': 'Location',
        'description': 'Locations include cities, dungeons, any place really.'
    },
    {
        'name': 'Historical Fragments',
        'description': 'Historical Fragments are events that happened. They are split into single events for simplicity.'
    },
    {
        'name': 'Objects',
        'description': 'Objects are well, things.'
    },
    {
        'name': 'World Data',
        'description': 'World Data is lore that is constant eg: magic exists.'
    },
    {
        'name': 'Connective',
        'description': 'Connective tables help weave the web of data.'
    },
    {
        'name': 'Utility',
        'description': 'Utility endpoints are general tools.'
    }
]

class ActorPostRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    title: str
    actor_age: int
    class_id: int
    actor_level: int
    background_id: int
    job: str
    actor_role: str
    race_id: int
    sub_race_id: int
    alignment: str
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int
    ideal: str
    bond: str
    flaw: str
    appearance: str
    strengths: str
    weaknesses: str
    notes: str

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    "first_name": "Smelly",
                    "middle_name": "Von",
                    "last_name": "Smellster",
                    "title": "Things like Dr., Arch Mage, that kind of thing.",
                    "actor_age": 33,
                    "class_id": 1,
                    "actor_level": 1,
                    "background_id": 1,
                    "job": "What job does this Actor do? Are they homeless? A Blacksmith?",
                    "actor_role": "Why is this character in your story? Are they a villian? Sidekick?",
                    "race_id": 0,
                    "sub_race_id": 0,
                    "alignment": "NN",
                    "strength": 0,
                    "dexterity": 0,
                    "constitution": 0,
                    "intelligence": 0,
                    "wisdom": 0,
                    "charisma": 0,
                    "ideal": "A text description of what ideals the Actor strives for. Kindness, Equality, Power, that sort of thing.",
                    "bond": "A text description of something that the Actor cares a great deal for. Person, place, Thing, w/e.",
                    "flaw": "A text description of a specific flaw the Actor has. Something that usually can be exploited.",
                    "appearance": "A text description of what the Actor looks like. As long as needed.",
                    "strengths": "A text description of what the Actor is good at. As long as needed.",
                    "weaknesses": "A text description of what the Actor struggles with. What they are bad at. As long as needed.",
                    "notes": "A place for any additional notes not covered previously."
                }
            ]
        }
    }

class ActorPutRequest(BaseModel):
    id: int
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    title: str | None = None
    actor_age: int | None = None
    class_id: int | None = None
    actor_level: int | None = None
    background_id: int | None = None
    job: str | None = None
    actor_role: str | None = None
    race_id: int | None = None
    sub_race_id: int | None = None
    alignment: str | None = None
    strength: int | None = None
    dexterity: int | None = None
    constitution: int | None = None
    intelligence: int | None = None
    wisdom: int | None = None
    charisma: int | None = None
    ideal: str | None = None
    bond: str | None = None
    flaw: str | None = None
    appearance: str | None = None
    strengths: str | None = None
    weaknesses: str | None = None
    notes: str | None = None

class FactionPostRequest(BaseModel):
    faction_name: str
    faction_description: str
    goals: str
    faction_values: str
    faction_income_sources: str
    faction_expenses: str

    model_config = {
        "json_schema_extra": {
            'examples': [
                {
                    "faction_name": "The name of the group",
                    "faction_description": "A description of who what and why they are",
                    "goals": "What does this group hope to acheive?",
                    "faction_values": "What do they hold as important in this group?",
                    "faction_income_sources": "Where is the cash coming from?",
                    "faction_expenses": "Where is the cash going?"
                }
            ]
        }
    }

class ActorAOnBRelationsPostRequest(BaseModel):
    item_a_id: int
    item_b_id: int
    overall: str
    economically: str
    power_dynamic: str

class FactionPutRequest(BaseModel):
    id: int
    faction_name: str | None = None
    faction_description: str | None = None
    goals: str | None = None
    faction_values: str | None = None
    faction_income_sources: str | None = None
    faction_expenses: str | None = None

class LocationPostRequest(BaseModel):
    location_name: str
    location_type: str
    location_description: str
    sights: str
    smells: str
    sounds: str
    feels: str
    tastes: str
    coordinates: str

class LocationPutRequest(BaseModel):
    id: int
    location_name: str | None = None
    location_type: str | None = None
    location_description: str | None = None
    sights: str | None = None
    smells: str | None = None
    sounds: str | None = None
    feels: str | None = None
    tastes: str | None = None
    coordinates: str | None = None

class HistoryPostRequest(BaseModel):
    event_name: str
    event_year: int
    event_description: str

class HistoryPutRequest(BaseModel):
    id: int
    event_name: str | None = None
    event_year: int | None = None
    event_description: str | None = None

class ObjectPostRequest(BaseModel):
    object_name: str
    object_description: str
    object_value: int
    rarity: str

class ObjectPutRequest(BaseModel):
    id: int
    object_name: str | None = None
    object_description: str | None = None
    object_value: int | None = None
    rarity: str | None = None

class WorldDataPostRequest(BaseModel):
    data_name: str
    data_description: str

class WorldDataPutRequest(BaseModel):
    id: int
    data_name: str | None = None
    data_description: str | None = None

class PostDataRequest(BaseModel):
    currentOpen: dict
    selectedId: int

class GetEndDataRequest(BaseModel):
    targetEnd: str

class GetSelfConnectiveData(BaseModel):
    targetSelfConnective: str

class PostFactionMember(BaseModel):
    actor_id: int
    actor_role: str
    faction_id: int
    relative_power: int

class PutFactionMember(BaseModel):
    id: int | None = None
    actor_id: int | None = None
    actor_role: str | None = None
    faction_id: int | None = None
    relative_power: int | None = None

class PostResident(BaseModel):
    actor_id: int
    location_id: int

class PostInvolvedHistoryActor(BaseModel):
    actor_id: int
    history_id: int

class PostLocationToFaction(BaseModel):
    faction_id: int
    faction_power: str
    faction_presence: str
    location_id: int
    notes: str

class PostInvolvedHistoryLocation(BaseModel):
    history_id: int
    location_id: int

class PostHistoryFaction(BaseModel):
    history_id: int
    faction_id: int

class PostHistoryObject(BaseModel):
    history_id: int
    object_id: int

class PostHistoryWorldData(BaseModel):
    history_id: int
    world_data_id: int

class PostObjectToOwner(BaseModel):
    object_id: int
    actor_id: int

class PostFactionAOnBRelations(BaseModel):
    item_a_id: int
    item_b_id: int
    overall: str
    opinion: str
    politically: str
    economically: str