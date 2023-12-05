import psycopg2 as pg
import psycopg2.extras
import os, csv
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')

def open_csv_and_query(query:str, file_location:str, cursor:pg.extensions.cursor):
    with open(file_location) as f:
        values = csv.reader(f)
        headers = next(values)
        
        for i in values:
            cursor.execute(query, i)

def make_curs_and_query(query:str, conn:pg.extensions.connection) -> dict:
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curs.execute(query)
    result = curs.fetchall()
    # answer = result[0]
    yield result
    curs.close()

def make_curs_query_commit(query:str, conn:pg.extensions.connection):
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield curs.execute(query) # should yield .fetchall
    except Exception as e:
        yield e
    finally:
        curs.close()

def single_item_table_query(table_name:str, id:int) -> str:
    query = f"""
        SELECT * FROM {table_name} x
        WHERE x.id = {id};
    """
    return query

def make_query_two_tables(table_1:str, table_2:str, table_2_id:str, id:int) -> str:
    query = f"""
        SELECT * FROM {table_1} x
        JOIN {table_2} y ON x.id = y.{table_2_id}
        WHERE x.id = {id};
    """
    return query

def multi_query(table_1:str, table_2_list_w_id:list, id:int, conn:pg.extensions.connection):
    answer_list = []
    for i, j in table_2_list_w_id:
        query = make_query_two_tables(table_1, i, j, id)
        answer = make_curs_and_query(query, conn)
        answer_list.append(answer)
    return answer_list

def find_column_names(table_name:str) -> list:
    conn = pg.connect(db_url)
    curs = conn.cursor()
    curs.execute(f"SELECT * FROM {table_name} LIMIT 0;")
    column_names = [desc[0] for desc in curs.description]
    curs.close()
    conn.close()
    return column_names[1:]

class Pg_Table:
    def __init__(self, table_name:str) -> None:
        self.table_name = table_name
        self.columns = find_column_names(self.table_name)
        self.insert_query_variables = str(tuple(self.columns)).replace("\'", "")
        self.insert_query_values = str("%s, "*len(self.columns))[:-2]

    def build_query(self):
        query_full = f"""
            INSERT INTO {self.table_name} {self.insert_query_variables}
            VALUES ({self.insert_query_values})
        """
        return query_full
    
    def select_all(self):
        query_full = f'SELECT * FROM {self.table_name}'
        return query_full

classes_table = Pg_Table("classes")
background_table = Pg_Table("background")
race_table = Pg_Table("race")
sub_race_table = Pg_Table("sub_race")
actor_table = Pg_Table("actor")
faction_table = Pg_Table("faction")
faction_a_on_b_relations_table = Pg_Table("faction_a_on_b_relations")
faction_members_table = Pg_Table("faction_members")
location_table = Pg_Table('location_')
location_to_faction_table = Pg_Table('location_to_faction')
location_dungeon_table = Pg_Table('location_dungeon')
location_city_table = Pg_Table('location_city')
location_city_districts_table = Pg_Table('location_city_districts')
residents_table = Pg_Table('residents')
historical_fragments_table = Pg_Table('historical_fragments')
involved_history_actor_table = Pg_Table('involved_history_actor')
involved_history_location_table = Pg_Table('involved_history_location')
object_table = Pg_Table('object_')
involved_history_object_table = Pg_Table('involved_history_object')
world_data_table = Pg_Table('world_data')
involved_history_world_data_table = Pg_Table('involved_history_world_data')

class ActorItem(BaseModel):
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

