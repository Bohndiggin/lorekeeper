from contextlib import asynccontextmanager
import psycopg2 as pg
import psycopg2.extras
import os
import utils
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')
conn = pg.connect(db_url)
curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
generic_select_query = 'SELECT * FROM {} LIMIT 10;'

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server starting up")

    yield
    conn.close()
    print("Server Shutdown Complete")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def homepage():
    pass

@app.get("/actor")
async def actor_get():
    query = generic_select_query.format('actor')
    answer = utils.make_curs_and_query(query, conn)
    # print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)


@app.get('/actor/')
async def actor_get_one(id:int = 0):
    query = f"""
        SELECT * FROM actor a
        JOIN classes c ON c.id = a.class_id
        JOIN background b ON b.id = a.background_id
        JOIN race r ON r.id = a.race_id
        WHERE a.id = {id};
    """
    answer = utils.make_curs_and_query(query, conn)
    # print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/faction')
async def faction_get():
    query = generic_select_query.format('faction')
    answer = utils.make_curs_and_query(query, conn)
    print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/faction/')
async def faction_get_one(id:int = 0):
    query_list = [
        ['faction_members', 'faction_id'],
        ['faction_a_on_b_relations', 'faction_a_id'],
        ['location_to_faction', 'faction_id']
    ]
    answer_list = utils.multi_query('faction', query_list, id, conn)

    # query_list_two = [
    #     ['']
    # ]

    # answer_list.append(utils.multi_query('location'))
    print(answer_list)
    answers = []
    for row in answer_list:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/location')
async def location_get():
    query = generic_select_query.format('location_')
    answer = utils.make_curs_and_query(query, conn)
    print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/location/')
async def location_get_one(id:int = 0):
    query_list = [
        ['location_to_faction', 'location_id'],
        ['location_dungeon', 'location_id'],
        ['location_city', 'location_id'],
        ['location_city_districts', 'city_id'],
        ['residents', 'city_id']
    ]
    answer_list = utils.multi_query('location_', query_list, id, conn)
    print(answer_list)
    answers = []
    for row in answer_list:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/historical-fragments')
async def historical_fragments_get():
    query = generic_select_query.format('historical_fragments')
    answer = utils.make_curs_and_query(query, conn)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/historical-fragments/')
async def historical_fragments_get_one(id:int = 0):
    query_list = [
        ['involved_history_actor', 'historical_fragment_id'],
        ['involved_history_location', 'historical_fragment_id'],
        ['involved_history_object', 'historical_fragment_id'],
        ['involved_history_world_data', 'historical_fragment_id']
    ]
    answer_list = utils.multi_query('historical_fragments', query_list, id, conn)
    print(answer_list)
    answers = []
    for row in answer_list:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/object')
async def object_get():
    query = generic_select_query.format('object_')
    answer = utils.make_curs_and_query(query, conn)
    print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)

@app.get('/object/')
async def object_get_one(id:int = 0):
    query_list = [
        []
    ]

@app.get('/world-data')
async def world_data_get():
    query = generic_select_query.format('world_data')
    answer = utils.make_curs_and_query(query, conn)
    print(answer)
    answers = []
    for row in answer:
        answers.append(dict(row[0]))
    print(answers)