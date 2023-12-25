from contextlib import asynccontextmanager
import psycopg2 as pg
import psycopg2.extras
import os, json
import utils
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')
conn = pg.connect(db_url)
curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
generic_select_query = 'SELECT * FROM {};'

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
    conn.close()
    print("Server Shutdown Complete")

app = FastAPI(lifespan=lifespan)

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
# WRITE WAY TO GET JUST ONE OBJECT'S NAME
@app.get("/actor")
async def actor_get():
    return utils.actor_table.query_get_10(conn)

@app.get('/actor/')
async def actor_get_one(id:int = 0):
    return utils.actor_table.query_one_by_id(id, conn)

@app.get('/faction')
async def faction_get():
    return utils.faction_table.query_get_10(conn)

@app.get('/faction/')
async def faction_get_one(id:int = 0):
    return utils.faction_table.query_one_by_id(id, conn)

@app.get('/location')
async def location_get():
    return utils.location_table.query_get_10(conn)

@app.get('/location/')
async def location_get_one(id:int = 0):
    return utils.location_table.query_one_by_id(id, conn)

@app.get('/historical-fragments')
async def historical_fragments_get():
    return utils.historical_fragments_table.query_get_10(conn)

@app.get('/historical-fragments/')
async def historical_fragments_get_one(id:int = 0):
    return utils.historical_fragments_table.query_one_by_id(id, conn)

@app.get('/object')
async def object_get():
    return utils.object_table.query_get_10(conn)

@app.get('/object/')
async def object_get_one(id:int = 0):
    return utils.object_table.query_one_by_id(id, conn)

@app.get('/world-data')
async def world_data_get():
    return utils.world_data_table.query_get_10(conn)

@app.get('world-data/')
async def world_data_get_one(id:int = 0):
    return utils.world_data_table.query_one_by_id(id, conn)