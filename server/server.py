from contextlib import asynccontextmanager
import psycopg2 as pg
import psycopg2.extras
import os, json
from datetime import datetime
import server.utils as utils

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from server.server_meta import *

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

app.mount('/main', StaticFiles(directory='./client_browser', html=True), name='dmdms')

origins = [
    '*'
]

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
async def actor_post(body:ActorPostRequest):
    return utils.actor_table.post_data(body)

@app.get('/actor-names', tags=['Actors'])
async def actor_get_names():
    return utils.actor_table.get_all_named()

@app.get('/actor/', tags=['Actors'])
async def actor_get_one(id:int = 0):
    return utils.actor_table.query_one_by_id(id)

@app.delete('/actor/', tags=['Actors'])
async def actor_delete_one(id:int):
    return utils.actor_table.delete_row_w_dependancies(id)

@app.post('/actor/', tags=['Actors'])
async def actor_post_related(body):
    return body

@app.get('/faction', tags=['Faction'])
async def faction_get():
    return utils.faction_table.query_get_10()

@app.post('/faction', tags=['Faction'])
async def faction_post(body:FactionPostRequest):
    return utils.actor_table.post_data(body)

@app.get('/faction-names', tags=['Faction'])
async def faction_get_names():
    return utils.faction_table.get_all_named()

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
async def location_post(body:LocationPostRequest):
    return utils.location_table.post_data(body)

@app.get('/location-names', tags=['Location'])
async def location_get_names():
    return utils.location_table.get_all_named()

@app.get('/location/', tags=['Location'])
async def location_get_one(id:int = 0):
    return utils.location_table.query_one_by_id(id)

@app.delete('/location/', tags=['Location'])
async def loctaion_delete_one(id:int):
    return utils.location_table.delete_row_w_dependancies(id)

@app.get('/residents-post', tags=['Location'])
async def resident_post_one(location_id):
    print(location_id)
    return location_id

@app.get('/historical-fragments', tags=['Historical Fragments'])
async def historical_fragment_get():
    return utils.historical_fragment_table.query_get_10()

@app.post('/historical-fragments', tags=['Historical Fragments'])
async def historical_fregments_post(body:HistoricalFragmentsRequest):
    return utils.historical_fragment_table.post_data(body)

@app.get('/historical-fragments-names', tags=['Historical Fragments'])
async def historical_fragment_get_names():
    return utils.historical_fragment_table.get_all_named()

@app.get('/historical-fragments/', tags=['Historical Fragments'])
async def historical_fragment_get_one(id:int = 0):
    return utils.historical_fragment_table.query_one_by_id(id)

@app.get('/object', tags=['Objects'])
async def object_get():
    return utils.object_table.query_get_10()

@app.post('/object', tags=['Objects'])
async def object_post(body:ObjectRequest):
    return utils.object_table.post_data(body)

@app.get('/object-names', tags=['Objects'])
async def object_get_names():
    return utils.object_table.get_all_named()

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

@app.post('/world-data', tags=['World Data'])
async def world_data_post(body:WorldDataRequest):
    return utils.world_data_table.post_data(body)

@app.get('/world-data-names', tags=['World Data'])
async def world_data_get_names():
    return utils.world_data_table.get_all_named()

@app.post('/test-data-post')
async def post_data_test(body:PostDataRequest):
    return utils.recieve_connective_post(body)

@app.post('/query-endcaps')
async def get_endcap_data(body:GetEndcapDataRequest):
    return utils.all_tables[body.targetEndcap].get_all_named()

@app.get('/load-tables')
async def load_table_data():
    response = {}
    for i in utils.all_tables.values():
        column_data = i.get_columns()
        response[i.table_name_no_dunder] = column_data
    return response