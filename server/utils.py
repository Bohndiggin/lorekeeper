import psycopg2 as pg
from psycopg2 import sql
import psycopg2.extras
import os, csv
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')
generic_select_query = sql.SQL('SELECT * FROM {} LIMIT 10;')

def open_csv_and_query(query:str, file_location:str, cursor:pg.extensions.cursor):
    with open(file_location) as f:
        values = csv.reader(f)
        headers = next(values)
        for i in values:
            cursor.execute(query, i)

def unpack_answer(answer) -> list:
    answers_list = []
    for row in answer:
        answers_list.append(dict(row))
    return answers_list

def make_curs_and_query(query:sql.SQL) -> dict:
    with pg.connect(db_url) as conn:
        # print(query)
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(query)
        result = curs.fetchall()
    return result

def make_curs_query_commit(query:sql.SQL) -> str:
    with pg.connect(db_url) as conn:
        curs = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curs.execute(query)
        conn.commit()
    return ['sucess!']

def query_to_answer(query:str, query_object:dict) -> list:
    query = sql.SQL(query)
    query = query.format(**query_object)
    packed_answer = make_curs_and_query(query)
    answer = unpack_answer(packed_answer)
    return answer

class Pg_Table:
    """Basic Table Parent Class"""
    def __init__(self, table_name:str, table_id_name:str='id') -> None:
        self.table_name = table_name
        self.columns = self._find_column_names(self.table_name)
        insert_query_variables = str(tuple(self.columns)).replace("\'", "")
        insert_query_values = str("{}, "*len(self.columns))[:-2]
        self.insert_query = self._build_post_query(insert_query_variables, insert_query_values)
        # self.select_10_query = generic_select_query.format(self.table_name)
        self.table_id_name = table_id_name

    def _find_column_names(self, table_name:str) -> list:
        """Queries the database and gets the column names sans the id then returns them as a list"""
        conn = pg.connect(db_url)
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {table_name} LIMIT 0;")
        column_names = [desc[0] for desc in curs.description]
        curs.close()
        conn.close()
        return column_names[1:]

    def _build_post_query(self, insert_query_variables, insert_query_values) -> sql.SQL:
        """Private Function builds out the default/template query for posting data"""
        query_full = f"""
            INSERT INTO {self.table_name} {insert_query_variables}
            VALUES ({insert_query_values})
        """
        query_SQL = sql.SQL(query_full)
        # print(query_SQL)
        return query_SQL

    def post_data(self, data:list) -> list:
        """This Function uses the build_insert_query sql.SQL and a list of lists to add rows to the data"""
        data_returned = []
        for i in data:
            if len(i) != len(self.columns):
                error_message_dict = {}
                error_message_dict[data.index(i)] = 'ERROR: list length too short to process'
                data_returned += error_message_dict
                continue
            current_data = [sql.Literal(j) for j in i]
            current_query = self.insert_query
            current_query = current_query.format(*current_data)
            # print(current_query)
            data_returned += make_curs_query_commit(current_query)
        return data_returned

class InteractiveTable(Pg_Table):
    """Parent class for tables that will be directly interacted with by the user."""
    def __init__(self, table_name: str, proper_name:str, foreign_key_name:str, table_id_name: str = 'id') -> None:
        super().__init__(table_name, table_id_name)
        self.proper_name = proper_name
        self.foreign_key_name = foreign_key_name

    def select_all(self):
        """Function queries and returns all rows of table"""
        query_full = "SELECT * FROM {table_name};"
        query_full_object = {
            'table_name': self.table_name
        }
        return query_full, query_full_object

    def single_item_table_query(self, id:int) -> dict:
        query = """
            SELECT * FROM {sql_table_name} x
            WHERE x.id = {sql_id};
        """
        query = sql.SQL(query).format(sql_table_name = sql.Identifier(self.table_name), sql_id = sql.Literal(id))
        answer = make_curs_and_query(query)
        return answer

    def query_get_10(self) -> list:
        """Function queries and returns the first 10 of a table. TODO make it able to get next 10"""
        name_object = sql.Identifier(self.table_name)
        query = generic_select_query.format(name_object)
        answer = make_curs_and_query(query)
        answers = unpack_answer(answer)
        return answers

    def get_all_named(self) -> list[dict]:
        """Function returns a list of every item in the table, proper name only"""
        query = """
            SELECT x.id, x.{proper_name} FROM {table_name} x;
        """
        query_object = {
            'proper_name': sql.Identifier(self.proper_name),
            'table_name': sql.Identifier(self.table_name)
        }
        answer = query_to_answer(query, query_object)
        return answer

    def get_item_name(self, id:int) -> str:
        query = """
            SELECT x.{proper_name} FROM {table_name} x
            WHERE x.id = {id};
        """
        query_object = {
            'item_name': sql.Identifier(self.proper_name),
            'table_name': sql.Identifier(self.table_name),
            'id': sql.Literal(id)
        }
        answer = query_to_answer(query, query_object)
        return answer[0]

    def delete_row(self, id:int):
        """Function takes in an id and deletes the row with the matching id. It returns a sucess/fail"""
        query = """
                DELETE FROM {table_name}
                WHERE id = {id};
        """
        query = sql.SQL(query).format(table_name=sql.Identifier(self.table_name), id=sql.Literal(id))
        return make_curs_query_commit(query)

class BackgroundTable(Pg_Table):
    """Parent class for tables that will not be directly influenced by the user."""
    def __init__(self, table_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_name, table_id_name)

    def delete_row_with_id(self, id:int):
        pass

class ConnectiveTable(BackgroundTable):
    def __init__(self, table_name: str, first_table:'QueryableTable', second_table:'QueryableTable',  table_id_name: str = 'id') -> None:
        super().__init__(table_name, table_id_name)
        self.first_table = first_table
        self.second_table = second_table

    def query_three_tables(self, foreign_id_str:str, id:int) -> tuple[list, str]:
        """Function queries 3 tables, Left Middle and Right. It returns a value(the answer) and a key(the middle table name)"""
        query = """
            SELECT y.id, z.{right_proper_name}, y.{left_proper_name}, x.* FROM {middle_table_name} x
            JOIN {left_table_name} y ON x.{left_table_foreign_key_str} = y.id
            JOIN {right_table_name} z ON x.{right_table_foreign_key_str} = z.id
            WHERE {foreign_id_str} = {id};
        """
        query_object = {
            'right_proper_name': sql.Identifier(self.second_table.proper_name),
            'left_proper_name': sql.Identifier(self.first_table.proper_name),
            'middle_table_name': sql.Identifier(self.table_name),
            'left_table_name': sql.Identifier(self.first_table.table_name),
            'left_table_foreign_key_str': sql.Identifier(self.first_table.foreign_key_name),
            'right_table_name': sql.Identifier(self.second_table.table_name),
            'right_table_foreign_key_str': sql.Identifier(self.second_table.foreign_key_name),
            'foreign_id_str': sql.Identifier(foreign_id_str),
            'id': sql.Literal(id)
        }
        answer = query_to_answer(query, query_object)
        return answer, self.table_name

    def multi_delete(self, foreign_id_str:str, foreign_id:int):
        """Function takes in an id and deletes the row with the matching id. It returns a sucess/fail"""
        query = """
                DELETE FROM {table_name}
                WHERE {foreign_id_str} = {id};
        """
        query = sql.SQL(query).format(table_name=sql.Identifier(self.table_name), foreign_id_str=sql.Identifier(foreign_id_str), id=sql.Literal(foreign_id))
        return make_curs_query_commit(query)

class SelfConnectiveTable(ConnectiveTable):
    def __init__(self, table_name: str, first_table: 'QueryableTable', second_table: 'QueryableTable', foreign_keys:list, table_id_name: str = 'id') -> None:
        super().__init__(table_name, first_table, second_table, table_id_name)
        self.foreign_keys = foreign_keys

    def query_connected(self, id:int):
        query = """
            SELECT * FROM {table_name} x
            JOIN {connected_table} y ON y.id = x.{foreign_key_1}
            JOIN {connected_table} z ON z.id = x.{foreign_key_2}
            WHERE x.{foreign_key_1} = {id};
        """
        query_object = {
            'table_name': sql.Identifier(self.table_name),
            'connected_table': sql.Identifier(self.first_table.table_name),
            'foreign_key_1': sql.Identifier(self.foreign_keys[0]),
            'foreign_key_2': sql.Identifier(self.foreign_keys[1]),
            'id': sql.Literal(id)
        }
        answer = query_to_answer(query, query_object)
        return answer, self.table_name

class EndCapTable(InteractiveTable):
    def __init__(self, table_name: str, foreign_key_name: str, proper_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_name, proper_name, foreign_key_name, table_id_name)

class QueryableTable(InteractiveTable):
    def __init__(self, table_name: str, foreign_key_name: str, proper_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_name, proper_name, foreign_key_name, table_id_name)
        self.endcap_table_list = []
        self.connective_table_list = []
        self.self_connective_table_list = []

    def connect_to_endcaps(self, trait_table_list:list) -> None:
        """Function connects this table to trait tables (ReferrableTable)"""
        self.endcap_table_list = [table for table in trait_table_list if type(table) == EndCapTable]

    def connect_to_connective_tables(self, middle_table_list:list) -> None:
        """Function connects this table to middle/joining tables"""
        self.connective_table_list = [table for table in middle_table_list if type(table) == ConnectiveTable]

    def connect_to_self_connective_tables(self, self_connective_tables:list):
        """Function connects this table to rubberbanding tables"""
        self.self_connective_table_list = [table for table in self_connective_tables if type(table) == SelfConnectiveTable]

    def query_two_tables(self, table_2_obj:EndCapTable, id:int) -> tuple[list, str]:
        """Function queries the object's table and one other, an EndCapTable and returns a list of answers and the name of the table queried, as a string"""
        query = """
            SELECT x.id, y.* FROM {table_1_name} x
            JOIN {table_2_name} y ON x.{foreign_key} = y.{table_1_id_name}
            WHERE x.id = {id};
        """
        query_object = {
            'table_1_name': sql.Identifier(self.table_name),
            'table_2_name': sql.Identifier(table_2_obj.table_name),
            'foreign_key': sql.Identifier(table_2_obj.foreign_key_name),
            'table_1_id_name': sql.Identifier(table_2_obj.table_id_name),
            'id': sql.Literal(id)
        }
        answer = query_to_answer(query, query_object)
        return answer, table_2_obj.table_name

    def multi_dual_query(self, id:int) -> dict:
        """Function runs multiple iterations of query_two_tables and returns a dictionary."""
        answer_dict = {}
        for table in self.endcap_table_list:
            value, key = self.query_two_tables(table, id)
            answer_dict[key] = value
        return answer_dict
    
    def multi_tri_query(self, id:int) -> dict:
        """Function runs multiple iterations of query_three_tables and returns a dictionary."""
        answer_dict = {}
        for table in self.connective_table_list:
            value, key = table.query_three_tables(self.foreign_key_name, id)
            answer_dict[key] = value
        return answer_dict
    
    def multi_self_connected_query(self, id:int) -> dict:
        """Funciton queries the self connected table associated with this object, if any."""
        answer_dict = {}
        for table in self.self_connective_table_list:
            value, key = table.query_connected(id)
            answer_dict[key] = value
        return answer_dict

    def query_one_by_id(self, id:int) -> dict:
        """Function finds everything associated with a single item and returns a dictionary"""
        answer = {}
        answer['overview'] = self.single_item_table_query(id)[0]
        answer['self-connective'] = self.multi_self_connected_query(id)
        answer['traits'] = self.multi_dual_query(id)
        answer['related'] = self.multi_tri_query(id)
        return answer
    
    def delete_row_w_dependancies(self, foreign_key:str, id:int):
        """Function finds everything related to a row in a table and deletes them then the row in the table itself"""
        for i in self.self_connective_table_list:
            i.multi_delete(foreign_key, id)
        for i in self.connective_table_list:
            i.multi_delete(self.foreign_key_name, id)
        self.delete_row(id)

classes_table = EndCapTable("classes", 'class_id', 'class_name')
background_table = EndCapTable("background", 'background_id', 'background_name')
race_table = EndCapTable("race", 'race_id', 'race_name')
sub_race_table = EndCapTable("sub_race", 'sub_race_id', 'sub_race_name')
actor_table = QueryableTable("actor", 'actor_id', 'first_name')

faction_table = QueryableTable("faction", 'faction_id', 'faction_name')
faction_a_on_b_relations_table = SelfConnectiveTable("faction_a_on_b_relations", faction_table, faction_table, ['faction_a_id', 'faction_b_id'])
faction_members_table = ConnectiveTable("faction_members", faction_table, actor_table)

location_table = QueryableTable('location_', 'location_id', 'location_name')
location_to_faction_table = ConnectiveTable('location_to_faction', location_table, faction_table)
location_dungeon_table = ConnectiveTable('location_dungeon', location_table, location_table)
location_city_table = ConnectiveTable('location_city', location_table, location_table)
location_city_districts_table = ConnectiveTable('location_city_districts', location_table, location_table)
residents_table = ConnectiveTable('residents', location_table, actor_table)
location_flora_fauna_table = "table type of end or something. not middle table but bookend typething"

historical_fragments_table = QueryableTable('historical_fragments', 'historical_fragment_id', 'event_name')
involved_history_actor_table = ConnectiveTable('involved_history_actor', historical_fragments_table, actor_table)
involved_history_location_table = ConnectiveTable('involved_history_location', historical_fragments_table, location_table)
involved_history_faction_table = ConnectiveTable('involved_history_faction', historical_fragments_table, faction_table)

object_table = QueryableTable('object_', 'object_id', 'object_name')
involved_history_object_table = ConnectiveTable('involved_history_object', object_table, historical_fragments_table)
object_to_owner_table = ConnectiveTable('object_to_owner', object_table, actor_table)

world_data_table = QueryableTable('world_data', 'world_data_id', 'data_name')
involved_history_world_data_table = ConnectiveTable('involved_history_world_data', historical_fragments_table, world_data_table)

# Here we connect up the tables

actor_table.connect_to_endcaps([classes_table, background_table, race_table, sub_race_table])
actor_table.connect_to_connective_tables([faction_members_table, residents_table, involved_history_actor_table])



faction_table.connect_to_connective_tables([faction_members_table, location_to_faction_table, historical_fragments_table])
faction_table.connect_to_self_connective_tables([faction_a_on_b_relations_table])

location_table.connect_to_endcaps([location_city_table])
location_table.connect_to_connective_tables([location_to_faction_table, residents_table, involved_history_location_table])

historical_fragments_table.connect_to_endcaps([])
historical_fragments_table.connect_to_connective_tables([involved_history_actor_table, involved_history_faction_table, involved_history_location_table, involved_history_object_table, involved_history_world_data_table])

object_table.connect_to_endcaps([])
object_table.connect_to_connective_tables([involved_history_object_table, object_to_owner_table])

world_data_table.connect_to_endcaps([])
world_data_table.connect_to_connective_tables([involved_history_world_data_table])