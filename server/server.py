from contextlib import asynccontextmanager
import psycopg2 as pg
import psycopg2.extras
import os, json
from datetime import datetime
import utils
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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

load_dotenv()

def unpack_answer(answer):
    answers_list = []
    for row in answer:
        for i in range(len(row)):
            answers_list.append(dict(row[i]))
    return answers_list

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server starting up")

    yield

    print("Server Shutdown Complete")

app = FastAPI(
    lifespan=lifespan,
    title="LoreKeeper",
    description=description,
    summary="The Keeper or Lore",
    version='0.1.2',
    openapi_tags=tags_metadata
)

app.mount('/main', StaticFiles(directory='../client_browser', html=True), name='dmdms')

origins = [
    '*'
]

class RequestBodyList(BaseModel):
    items_list: list
    # timestamp: datetime

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow_orgin_regex=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
async def homepage():
    pass

@app.get("/actor", tags=['Actors'])
async def actor_get():
    return utils.actor_table.query_get_10()

@app.post('/actor', tags=['Actors'])
async def actor_post(body:RequestBodyList):
    return utils.actor_table.post_data(body.items_list)

@app.get('/actor-names', tags=['Actors'])
async def actor_get_names():
    return utils.actor_table.get_all_named()

@app.get('/actor/', tags=['Actors'])
async def actor_get_one(id:int = 0):
    return utils.actor_table.query_one_by_id(id)

@app.delete('/actor/', tags=['Actors'])
async def actor_delete_one(id:int):
    return utils.actor_table.delete_row_w_dependancies(id)

@app.get('/faction', tags=['Faction'])
async def faction_get():
    return utils.faction_table.query_get_10()

@app.post('/faction', tags=['Faction'])
async def faction_post(body:RequestBodyList):
    return utils.actor_table.post_data(body.items_list)

@app.get('/faction/', tags=['Faction'])
async def faction_get_one(id:int = 0):
    return utils.faction_table.query_one_by_id(id)

@app.delete('/faction/', tags=['Faction'])
async def faction_delete_one(id:int):
    return utils.faction_table.delete_row_w_dependancies(id)

@app.get('/location', tags=['Location'])
async def location_get():
    return utils.location_table.query_get_10()

@app.post('/location', tags=['Location'])
async def location_post(body:RequestBodyList):
    return utils.location_table.post_data(body.items_list)

@app.get('/location/', tags=['Location'])
async def location_get_one(id:int = 0):
    return utils.location_table.query_one_by_id(id)

@app.delete('/location/', tags=['Location'])
async def loctaion_delete_one(id:int):
    return utils.location_table.delete_row_w_dependancies(id)

@app.get('/historical-fragments', tags=['Historical Fragments'])
async def historical_fragments_get():
    return utils.historical_fragments_table.query_get_10()

@app.post('/historical-fragments', tags=['Historical Fragments'])
async def historical_fregments_post(body:RequestBodyList):
    return utils.historical_fragments_table.post_data(body.items_list)

@app.get('/historical-fragments/', tags=['Historical Fragments'])
async def historical_fragments_get_one(id:int = 0):
    return utils.historical_fragments_table.query_one_by_id(id)

@app.get('/object', tags=['Objects'])
async def object_get():
    return utils.object_table.query_get_10()

@app.post('/object', tags=['Objects'])
async def object_post(body:RequestBodyList):
    return utils.object_table.post_data(body.items_list)

@app.get('/object/', tags=['Objects'])
async def object_get_one(id:int = 0):
    return utils.object_table.query_one_by_id(id)

@app.delete('/object/', tags=['Objects'])
async def object_delete_by_id(id:int):
    return utils.object_table.delete_row(id)

@app.get('/world-data', tags=['World Data'])
async def world_data_get():
    return utils.world_data_table.query_get_10()

@app.get('/world-data/', tags=['World Data'])
async def world_data_get_one(id:int = 0):
    return utils.world_data_table.query_one_by_id(id)