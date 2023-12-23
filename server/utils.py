import psycopg2 as pg
import psycopg2.extras
import os, csv
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')
generic_select_query = 'SELECT * FROM {} LIMIT 10;'

def unpack_answer(answer):
    answers_list = []
    for row in answer:
        for i in range(len(row)):
            answers_list.append(dict(row[i]))
    return answers_list

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
        SELECT x.id, y.* FROM {table_1} x
        JOIN {table_2} y ON x.id = y.{table_2_id}
        WHERE x.id = {id};
    """
    return query

def make_query_three_tables(middle_table:str, left_table:str, right_table:str, left_table_id:str, right_table_id:str, id:int) -> str:
    query = f"""
        SELECT * FROM {middle_table} x
        JOIN {left_table} y ON x.{left_table_id} = y.id
        JOIN {right_table} z ON x.{right_table_id} = z.id
        WHERE {left_table_id} = {id};
    """
    return query

def multi_dual_query(table_1:str, table_2_list_w_id:list, id:int, conn:pg.extensions.connection):
    answer_dict = {}
    for i, j in table_2_list_w_id:
        query = make_query_two_tables(table_1, i, j, id)
        answer = make_curs_and_query(query, conn)
        unpacked_answer = unpack_answer(answer)
        answer_dict[i] = unpacked_answer
        # print(unpacked_answer)
    return answer_dict

def multi_tri_query(left_table:str, left_table_id:str, table_M_R_list_w_id:list, conn:pg.extensions.connection, id:int):
    answer_dict = {}
    for i, j, k in table_M_R_list_w_id:
        query = make_query_three_tables(i, left_table, j, left_table_id, k, id)
        answer = make_curs_and_query(query, conn)
        unpacked_answer = unpack_answer(answer)
        answer_dict[i] = unpacked_answer
    return answer_dict

def single_item_full_multi_query(table:str, id:int, dual_query_list:list, table_id:str, middle_right_query_list:list, conn:pg.extensions.connection) -> dict:
    """Function finds everything associated with a single item and returns a dictionary"""
    answer = {}

    overview_query = single_item_table_query(table, id)
    overview = make_curs_and_query(overview_query, conn)
    answer['overview'] = unpack_answer(overview)[0]
    answer['traits'] = multi_dual_query(table, dual_query_list, id, conn)
    answer['related'] = multi_tri_query(table, table_id, middle_right_query_list, conn, id)
    
    return answer

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
        self.select_10_query = generic_select_query.format(self.table_name)

    def build_query(self):
        query_full = f"""
            INSERT INTO {self.table_name} {self.insert_query_variables}
            VALUES ({self.insert_query_values})
        """
        return query_full
    
    def select_all(self):
        query_full = f'SELECT * FROM {self.table_name}'
        return query_full
    
    def query_get_10(self, conn:pg.extensions.connection):
        answer = make_curs_and_query(self.select_10_query, conn)
        answers = unpack_answer(answer)
        return answers
    
class InteractableTable(Pg_Table):
    def __init__(self, table_name: str, table_id:str, query_list:list, middle_right_list:list) -> None:
        super().__init__(table_name)
        self.query_list = query_list
        self.middle_right_list = middle_right_list
        self.table_id = table_id

    def query_one_by_id(self, id:int, conn:pg.extensions.connection) -> dict:
        return single_item_full_multi_query(self.table_name, id, self.query_list, self.table_id, self.middle_right_list, conn)



classes_table = Pg_Table("classes")
background_table = Pg_Table("background")
race_table = Pg_Table("race")
sub_race_table = Pg_Table("sub_race")
actor_table = InteractableTable(
    "actor",
    'actor_id',
    [
        ['classes', 'id'],
        ['background', 'id'],
        ['race', 'id']
    ],
    [
        ['faction_members', 'faction', 'faction_id'],
        ['residents', 'location_', 'location_id'],
        ['involved_history_actor', 'historical_fragments', 'historical_fragment_id']
    ]
    )
faction_table = InteractableTable(
    "faction",
    'faction_id',
    [
        ['faction_a_on_b_relations', 'faction_a_id']
    ],
    [
        ['faction_members', 'actor', 'actor_id'],
        ['location_to_faction', 'faction', 'faction_id']
    ]
    )
faction_a_on_b_relations_table = Pg_Table("faction_a_on_b_relations")
faction_members_table = Pg_Table("faction_members")
location_table = InteractableTable(
    'location_',
    'location_id',
    [
        ['location_dungeon', 'location_id'],
        ['location_city', 'location_id'],
        ['location_city_districts', 'location_id']
    ],
    [
        ['residents', 'actor', 'actor_id'],
        ['location_to_faction', 'faction', 'faction_id']
    ]
    )
location_to_faction_table = Pg_Table('location_to_faction')
location_dungeon_table = Pg_Table('location_dungeon')
location_city_table = Pg_Table('location_city')
location_city_districts_table = Pg_Table('location_city_districts')
residents_table = Pg_Table('residents')
historical_fragments_table = InteractableTable(
    'historical_fragments',
    'historical_fragment_id',
    [
        ['involved_history_actor', 'historical_fragment_id'],
        ['involved_history_location', 'historical_fragment_id'],
        ['involved_history_object', 'historical_fragment_id'],
        ['involved_history_world_data', 'historical_fragment_id']
    ],
    [
        ['involved_history_actor', 'actor', 'actor_id'],
        ['involved_history_location', 'location_', 'location_id'],
        ['involved_history_object', 'object_', 'object_id'],
        ['involved_history_world_data', 'world_data', 'world_data_id']
    ]
    )
involved_history_actor_table = Pg_Table('involved_history_actor')
involved_history_location_table = Pg_Table('involved_history_location')
object_table = InteractableTable(
    'object_',
    'object_id',
    [
        ['involved_history_object', 'object_id']
    ],
    [
        ['involved_history_object', 'historical_fragments', 'historical_fragment_id']
    ]
    )
involved_history_object_table = Pg_Table('involved_history_object')
world_data_table = InteractableTable(
    'world_data',
    'world_data_id',
    [
        ['involved_history_world_data', 'world_data_id']
    ],
    [
        ['involved_history_world_data', 'historical_fragments', 'historical_fragment_id']
    ]
    )
involved_history_world_data_table = Pg_Table('involved_history_world_data')

