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

load_dotenv()
# db_url = os.getenv('CONNSTR')
# conn = pg.connect(db_url)
# curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
# generic_select_query = 'SELECT * FROM {};'

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

app = FastAPI(lifespan=lifespan)
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
# WRITE WAY TO GET JUST ONE OBJECT'S NAME
@app.get("/actor")
async def actor_get():
    return utils.actor_table.query_get_10()

@app.post('/actor')
async def actor_post(body:RequestBodyList):
    return utils.actor_table.post_data(body.items_list)

@app.get('/actor/')
async def actor_get_one(id:int = 0):
    return utils.actor_table.query_one_by_id(id)

@app.get('/faction')
async def faction_get():
    return utils.faction_table.query_get_10()

@app.get('/faction/')
async def faction_get_one(id:int = 0):
    return utils.faction_table.query_one_by_id(id)

@app.get('/location')
async def location_get():
    return utils.location_table.query_get_10()

@app.get('/location/')
async def location_get_one(id:int = 0):
    return utils.location_table.query_one_by_id(id)

@app.get('/historical-fragments')
async def historical_fragments_get():
    return utils.historical_fragments_table.query_get_10()

@app.get('/historical-fragments/')
async def historical_fragments_get_one(id:int = 0):
    return utils.historical_fragments_table.query_one_by_id(id)

@app.get('/object')
async def object_get():
    return utils.object_table.query_get_10()

@app.post('/object')
async def object_post(body:RequestBodyList):
    return utils.object_table.post_data(body.items_list)

@app.get('/object/')
async def object_get_one(id:int = 0):
    return utils.object_table.query_one_by_id(id)

@app.get('/world-data')
async def world_data_get():
    return utils.world_data_table.query_get_10()

@app.get('/world-data/')
async def world_data_get_one(id:int = 0):
    return utils.world_data_table.query_one_by_id(id)