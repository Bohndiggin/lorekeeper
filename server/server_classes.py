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

class HistoricalFragmentsRequest(BaseModel):
    event_name: str
    event_year: int
    event_description: str

class ObjectRequest(BaseModel):
    object_name: str
    object_description: str
    object_value: int
    rarity: str

class WorldDataRequest(BaseModel):
    data_name: str
    data_description: str