import psycopg2 as pg
from psycopg2 import sql
import psycopg2.extras
import os, csv
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')
generic_select_query = sql.SQL('SELECT * FROM {} LIMIT 10;')

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

def make_curs_and_query(query:sql.SQL, conn:pg.extensions.connection) -> dict:
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curs.execute(query)
    result = curs.fetchall()
    conn.commit()
    yield result
    curs.close()

def make_curs_query_commit(query:str, conn:pg.extensions.connection):
    curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        curs.execute(query)
        conn.commit()
        yield curs.fetchall(query) # should yield .fetchall
    except Exception as e:
        yield e
    finally:
        curs.close()

def single_item_table_query(table_name:str, id:int) -> str:
    query = """
        SELECT * FROM {sql_table_name} x
        WHERE x.id = {sql_id};
    """
    query = sql.SQL(query).format(sql_table_name = sql.Identifier(table_name), sql_id = sql.Literal(id))
    return query

def make_query_two_tables(table_1:str, table_2:str, table_2_id:str, id:int, table_1_id:str='id') -> str:
    query = """
        SELECT x.{}, y.* FROM {} x
        JOIN {} y ON x.{} = y.{}
        WHERE x.id = {};
    """
    query = sql.SQL(query)
    query = query.format(sql.Identifier(table_1_id),sql.Identifier(table_1),sql.Identifier(table_2),sql.Identifier(table_1_id),sql.Identifier(table_2_id),sql.Literal(id))
    return query

def make_query_three_tables(middle_table:str, left_table:str, right_table:str, left_table_id:str, right_table_id:str, id:int) -> str:
    query = """
        SELECT z.*, x.* FROM {} x
        JOIN {} y ON x.{} = y.id
        JOIN {} z ON x.{} = z.id
        WHERE {} = {};
    """
    query = sql.SQL(query)
    query = query.format(sql.Identifier(middle_table),sql.Identifier(left_table),sql.Identifier(left_table_id),sql.Identifier(right_table),sql.Identifier(right_table_id),sql.Identifier(left_table_id),sql.Literal(id))
    return query

def multi_dual_query(table_1:str, table_2_list_w_id:list, id:int, conn:pg.extensions.connection): # TODO Refactor all query stuff into the classes. Have it take in other objects as the argument.
    """Function runs multiple iterations of make_query_two_tables and returns a dictionary."""
    answer_dict = {}
    try:
        for i, j, k in table_2_list_w_id:
            query = make_query_two_tables(table_1, i, j, id, k)
            answer = make_curs_and_query(query, conn)
            unpacked_answer = unpack_answer(answer)
            answer_dict[i] = unpacked_answer
            # print(unpacked_answer)
    except:
        for i, j in table_2_list_w_id:
            query = make_query_two_tables(table_1, i, j, id)
            answer = make_curs_and_query(query, conn)
            unpacked_answer = unpack_answer(answer)
            answer_dict[i] = unpacked_answer
    # print(answer_dict)
    return answer_dict

def multi_tri_query(left_table:str, left_table_id:str, table_M_R_list_w_id:list, conn:pg.extensions.connection, id:int):
    """Function runs multiple iterations of make_query_three_tables and returns a dictionary of the answers
    INPUTS:
        left_table = the name of the left table,

        left_table_id = the id that other tables use to refer to the left table

        table_M_R_list_w_id = a list containing these elements [middle table name, right table name, right table id]

        conn = your postgreSQL connection

        id = the id of the item you need more info about
    """
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
    # Need a function to find proper name/item_name for each of the answers? Or uh. Table classes handle the queries??????
    overview_query = single_item_table_query(table, id)
    overview = make_curs_and_query(overview_query, conn)
    answer['overview'] = unpack_answer(overview)[0]
    answer['traits'] = multi_dual_query(table, dual_query_list, id, conn)
    # print(answer['traits'])
    answer['related'] = multi_tri_query(table, table_id, middle_right_query_list, conn, id)
    
    return answer

def find_column_names(table_name:str) -> list:
    """Queries the database and gets the column names sans the id then returns them as a list"""
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
        insert_query_variables = str(tuple(self.columns)).replace("\'", "")
        insert_query_values = str("%s, "*len(self.columns))[:-2]
        self.insert_query = self._build_post_query(insert_query_variables, insert_query_values)
        # self.select_10_query = generic_select_query.format(self.table_name)

    def _build_post_query(self, insert_query_variables, insert_query_values) -> sql.SQL:
        """Private Function builds out the default/template query for posting data"""
        query_full = f"""
            INSERT INTO {self.table_name} {insert_query_variables}
            VALUES ({insert_query_values})
        """
        query_SQL = sql.SQL(query_full)
        # print(query_SQL)
        return query_SQL

    
    def post_data(self, data:list, conn:pg.extensions.connection) -> list:
        """This Function uses the build_insert_query sql.SQL and a list of lists to add rows to the data"""
        data_returned = []
        for i in data:
            if len(i) != len(self.columns):
                error_message_dict = {}
                error_message_dict[data.index(i)] = 'ERROR: list length too short to process'
                data_returned += error_message_dict
                continue
            current_query = self.insert_query
            current_query = current_query.format(*i)
            data_returned += make_curs_and_query(current_query, conn)
        return data_returned
    
    def select_all(self):
        """Function should query and return all rows of table TODO make that actually happen"""
        query_full = "SELECT * FROM {table_name}"
        query_full_object = {
            'table_name': self.table_name
        }
        return query_full, query_full_object
    
    def query_get_10(self, conn:pg.extensions.connection) -> list:
        """Function queries and returns the first 10 of a table. TODO make it able to get next 10"""
        name_object = sql.Identifier(self.table_name)
        query = generic_select_query.format(name_object)
        answer = make_curs_and_query(query, conn)
        answers = unpack_answer(answer)
        return answers
    
    def delete_row(self):
        """Function takes in an id and deletes the row with the matching id. It returns a sucess/fail"""
        pass
    
class ReferrableTable(Pg_Table):
    def __init__(self, table_name: str, item_name: str = None) -> None:
        super().__init__(table_name)
        self.item_name = item_name

    def get_item_name(self, id:int, conn:pg.extensions.connection):
        query = """
            SELECT x.{item_name} FROM {table_name} x
            WHERE x.id = {id};
        """
        query_object = {
            'item_name': self.item_name,
            'table_name': self.table_name,
            'id': id
        }
        query = query.format(**query_object)
        packed_answer = make_curs_and_query(query, conn)
        answer = unpack_answer(packed_answer)
        return answer

class InteractableTable(ReferrableTable):
    def __init__(self, table_name: str, table_id:str, query_list:list, middle_right_list:list, name_str:str) -> None:
        super().__init__(table_name, name_str)
        self.query_list = query_list
        self.middle_right_list = middle_right_list
        self.table_id = table_id
        self.name_str = name_str
        self.trait_table_list = []
        self.middle_table_list = []
        self.right_table_list = []

    def query_one_by_id(self, id:int, conn:pg.extensions.connection) -> dict:
        return single_item_full_multi_query(self.table_name, id, self.query_list, self.table_id, self.middle_right_list, conn)
    
    def test(self, other:'InteractableTable'):
        pass

    def connect_to_traits(self, trait_table_list:list):
        for table in trait_table_list:
            if type(table) != ReferrableTable:
                continue
            self.trait_table_list.append(table)

    def _connect_to_trait(self, trait_table:ReferrableTable):
        self.trait_table_list += trait_table

    def connect_to_middle(self, middle_table):
        """Function connects this table to middle/joining tables. It returns nothing but it allows me to move singe item full multi query inside"""
        pass

    def connect_to_right(self, right_table):
        pass



classes_table = ReferrableTable("classes", 'class_name')
background_table = ReferrableTable("background", 'background_name')
race_table = ReferrableTable("race", 'race_name')
sub_race_table = ReferrableTable("sub_race", 'sub_race_name')
actor_table = InteractableTable(
    "actor",
    'actor_id',
    [
        ['classes', 'id', 'class_id'],
        ['background', 'id', 'background_id'],
        ['race', 'id', 'race_id'],
        ['sub_race', 'id', 'sub_race_id']
    ],
    [
        ['faction_members', 'faction', 'faction_id'],
        ['residents', 'location_', 'location_id'],
        ['involved_history_actor', 'historical_fragments', 'historical_fragment_id']
    ],
    'first_name'
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
    ],
    'faction_name'
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
    ],
    'location_name'
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
    ],
    'event_name'
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
        ['involved_history_object', 'historical_fragments', 'historical_fragment_id'],
        ['object_to_owner', 'actor', 'actor_id']
    ],
    'object_name'
    )
involved_history_object_table = Pg_Table('involved_history_object')
object_to_owner_table = Pg_Table('object_to_owner')
world_data_table = InteractableTable(
    'world_data',
    'world_data_id',
    [
        ['involved_history_world_data', 'world_data_id']
    ],
    [
        ['involved_history_world_data', 'historical_fragments', 'historical_fragment_id']
    ],
    'data_name'
    )
involved_history_world_data_table = Pg_Table('involved_history_world_data')

# print(actor_table.get_item_name())
# CONNECT_TO_Middle connect_to_right