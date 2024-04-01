import psycopg2 as pg
from psycopg2 import sql
import psycopg2.extras
import os, csv
from pydantic import BaseModel
from dotenv import load_dotenv
from server.server_meta import *
from server.database.engine import *
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import update, select, inspect


load_dotenv()

db_url = os.getenv('DATABASE_URL')
generic_select_query = sql.SQL('SELECT * FROM {} LIMIT 10;')

Session = sessionmaker(bind=engine)
# session = Session()


all_tables: dict['Pg_Table'] = {}

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

def clean_endpoint(endpoint:str) -> str:
    no_slash = endpoint[1:]
    underscores = no_slash.replace('-', '_')
    with_table = underscores + '_table'
    return with_table

def clean_table(table_name:str) -> str:
    underscores = table_name.replace('-', '_')
    with_table = underscores + '_table'
    no_dunder = with_table.replace('__', '_')
    return no_dunder

def get_endcaps(body):
    pass

class Pg_Table:
    """Basic Table Parent Class"""
    def __init__(self, table_type, table_name:str, table_id_name:str='id') -> None:
        self.table_type = table_type
        self.table_name = table_name
        self.table_id_name = table_id_name
        temp_name = table_name + '_table'
        self.table_name_no_dunder = temp_name.replace('__', '_')
        all_tables[self.table_name_no_dunder] = self

    def clean_response_multi(self, response:list) -> list[dict]:
        results_list = [row[0].__dict__ for row in response]
        for i in results_list:
            i.pop('_sa_instance_state')
        return results_list

    def post_data(self, data) -> list:
        """This Function uses the build_insert_query sql.SQL and a dict with keywords to add a row to the database"""
        data_dict = dict(data)
        new_row = self.table_type(**data_dict)
        with Session() as session:
            session.add(new_row)
            session.commit()

    def get_columns(self) -> list:
        """Function to get a list of columns so you can make sure user is supplying all the needed data"""
        inspector = inspect(engine)
        columns = inspector.get_columns(self.table_name)
        columns_and_types = {column['name']: str(column['type']) for column in columns}
        return columns_and_types

class InteractiveTable(Pg_Table):
    """Parent class for tables that will be directly interacted with by the user."""
    def __init__(self, table_type,  table_name: str, proper_name:str, foreign_key_name:str, table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, table_id_name)
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
        """Function to query for one row based on the id."""
        query = select(self.table_type).where(self.table_type.id == id)
        with Session() as session:
            result = session.execute(query).all()[0][0]
            dict_results = result.__dict__
            dict_results.pop('_sa_instance_state')
        return dict_results

    def query_get_10(self) -> list:
        """Function queries and returns the first 10 of a table. TODO make it able to get next 10"""
        with Session() as session:
            results = session.query(self.table_type).limit(10).all()
            dict_results = [row.__dict__ for row in results]
            for i in dict_results:
                i.pop('_sa_instance_state')
        return dict_results

    def get_all_named(self) -> list[dict]:
        """Function returns a list of every item in the table, proper name only"""
        with Session() as session:
            results = session.query(self.table_type).all()
            dict_results = [row.__dict__ for row in results]
        for i in dict_results:
            i.pop('_sa_instance_state')
        for i in dict_results:
            i['proper_name'] = i[self.proper_name]
            del i[self.proper_name]
        return dict_results

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

    def put_data(self, data):
        """Function takes in data and updates the proper row of the database. It returns a number of rows updated."""
        data = dict(data)
        data['id'] = data['id'] + 1
        with Session() as session:
            session.execute(update(self.table_type), [data])
            session.commit()


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
    def __init__(self, table_type, table_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, table_id_name)

    def delete_row_with_id(self, id:int):
        pass

class ConnectiveTable(BackgroundTable):
    def __init__(self, table_type, table_name: str, first_table:'QueryableTable', second_table:'QueryableTable',  table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, table_id_name)
        self.first_table = first_table
        self.second_table = second_table

    def query_three_tables(self, foreign_id_str:str, id:int) -> tuple[list, str]:
        """Function queries 3 tables, Left Middle and Right. It returns a value(the answer) and a key(the middle table name)"""
        proper_name_first_table = getattr(self.first_table.table_type, self.first_table.proper_name)
        proper_name_second_table = getattr(self.second_table.table_type, self.second_table.proper_name)
        query = select(self.table_type, proper_name_first_table, proper_name_second_table).join(self.second_table.table_type).join(self.first_table.table_type)
        with Session() as session:
            result = session.execute(query).all()
        answer = self.clean_response_multi(result)
        parsed_answer = []
        for i in range(len(answer)):
            if answer[i][foreign_id_str] == id:
                temp_dict = {}
                temp_dict[self.first_table.proper_name] = result[i][1]
                temp_dict[self.second_table.proper_name] = result[i][2]
                answer_dict = dict(temp_dict, **answer[i])
                parsed_answer.append(answer_dict)
        return parsed_answer, self.table_name

    def multi_delete(self, foreign_id_str:str, foreign_id:int):
        """Function takes in an id and deletes the row with the matching id. It returns a sucess/fail"""
        query = """
                DELETE FROM {table_name}
                WHERE {foreign_id_str} = {id};
        """
        query = sql.SQL(query).format(table_name=sql.Identifier(self.table_name), foreign_id_str=sql.Identifier(foreign_id_str), id=sql.Literal(foreign_id))
        return make_curs_query_commit(query)

class SelfConnectiveTable(ConnectiveTable):
    def __init__(self, table_type, table_name: str, first_table: 'QueryableTable', second_table: 'QueryableTable', foreign_keys:list, table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, first_table, second_table, table_id_name)
        self.foreign_keys = foreign_keys
        self.first_table_proper_name = getattr(self.first_table.table_type, self.first_table.proper_name)
        self.second_table_id_proper_name = getattr(self.second_table.table_type, self.second_table.proper_name)

    def query_connected(self, id:int):
        # Create an alias for the faction table
        FactionB = aliased(self.second_table.table_type)

        # Build the query
        query = select(self.table_type, self.first_table.table_type.faction_name, FactionB.faction_name).\
            select_from(
                self.table_type.__table__.join(self.first_table.table_type, self.table_type.faction_a_id == self.first_table.table_type.id).\
                join(FactionB, self.table_type.faction_b_id == FactionB.id)
            ).\
            where(self.table_type.faction_a_id == id)

        # Execute query
        with Session() as session:
            result = session.execute(query).all()

        # Clean answer
        answer = self.clean_response_multi(result)
        parsed_answer = []
        for i in range(len(answer)):
            if answer[i]['id'] == id:
                temp_dict = {}
                temp_dict[self.first_table.proper_name] = result[i][1]
                temp_dict[self.second_table.proper_name] = result[i][2]
                answer_dict = dict(temp_dict, **answer[i])
                parsed_answer.append(answer_dict)

        return parsed_answer, self.table_name

class EndCapTable(InteractiveTable):
    def __init__(self, table_type, table_name: str, foreign_key_name: str, proper_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, proper_name, foreign_key_name, table_id_name)

class QueryableTable(InteractiveTable):
    def __init__(self, table_type,  table_name: str, foreign_key_name: str, proper_name: str, table_id_name: str = 'id') -> None:
        super().__init__(table_type, table_name, proper_name, foreign_key_name, table_id_name)
        self.endcap_table_list = []
        self.connective_table_list = []
        self.self_connective_table_list = []

    def connect_to_endcaps(self, trait_table_list:list) -> None:
        """Function connects this table to trait tables (ReferrableTable)"""
        self.endcap_table_list = [table for table in trait_table_list if type(table) == EndCapTable]

    def connect_to_connective_tables(self, middle_table_list:list) -> None:
        """Function connects this table to middle/joining tables"""
        self.connective_table_list = [table for table in middle_table_list if type(table) == ConnectiveTable]
        self.connective_table_dict = {}
        for i in self.connective_table_list:
            self.connective_table_dict[i.table_name_no_dunder] = i

    def connect_to_self_connective_tables(self, self_connective_tables:list):
        """Function connects this table to rubberbanding tables"""
        self.self_connective_table_list = [table for table in self_connective_tables if type(table) == SelfConnectiveTable]

    def query_two_tables(self, table_2_obj:EndCapTable, id:int) -> tuple[list, str]:
        """Function queries the object's table and one other, an EndCapTable and returns a list of answers and the name of the table queried, as a string"""
        query = select(table_2_obj.table_type, self.table_type.id).join(table_2_obj.table_type).filter(self.table_type.id == id)
        with Session() as session:
            result = session.execute(query).all()
            answer = self.clean_response_multi(result)
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
        answer['overview'] = self.single_item_table_query(id)
        answer['self-connective'] = self.multi_self_connected_query(id)
        answer['traits'] = self.multi_dual_query(id)
        answer['related'] = self.multi_tri_query(id)
        return answer

    def call_connected_table(self, selected_table:ConnectiveTable, self_id:int, ext_id:int):
        """function takes in a specific table that it is connected to and will call that table's post_data function passing in the correct ids"""
        post_data = {}

        if selected_table.first_table == self:
            post_data[selected_table.second_table.foreign_key_name] = ext_id
        if selected_table.second_table == self:
            post_data[selected_table.first_table.foreign_key_name] = ext_id
        post_data[self.foreign_key_name] = self_id
        return selected_table.post_data(post_data)

    def delete_row_w_dependancies(self, foreign_key:str, id:int):
        """Function finds everything related to a row in a table and deletes them then the row in the table itself"""
        for i in self.self_connective_table_list:
            i.multi_delete(foreign_key, id)
        for i in self.connective_table_list:
            i.multi_delete(self.foreign_key_name, id)
        self.delete_row(id)

class_table = EndCapTable(Class_, "class", 'class_id', 'class_name')
background_table = EndCapTable(Background, "background", 'background_id', 'background_name')
race_table = EndCapTable(Race, "race", 'race_id', 'race_name')
sub_race_table = EndCapTable(SubRace, "sub_race", 'sub_race_id', 'sub_race_name')
actor_table = QueryableTable(Actor, "actor", 'actor_id', 'first_name')

faction_table = QueryableTable(Faction, "faction", 'faction_id', 'faction_name')
faction_a_on_b_relations_table = SelfConnectiveTable(FactionAOnBRelations, "faction_a_on_b_relations", faction_table, faction_table, ['faction_a_id', 'faction_b_id'])
faction_members_table = ConnectiveTable(FactionMembers, "faction_members", faction_table, actor_table)

location_table = QueryableTable(Location, 'location_', 'location_id', 'location_name')
location_to_faction_table = ConnectiveTable(LocationToFaction, 'location_to_faction', location_table, faction_table)
location_dungeon_table = ConnectiveTable(LocationDungeon, 'location_dungeon', location_table, location_table)
location_city_table = ConnectiveTable(LocationCity, 'location_city', location_table, location_table)
location_city_districts_table = ConnectiveTable(LocationCityDistricts, 'location_city_districts', location_table, location_table)
residents_table = ConnectiveTable(Resident, 'residents', location_table, actor_table)
location_flora_fauna_table = "table type of end or something. not middle table but bookend typething"

history_table = QueryableTable(History, 'history', 'history_id', 'event_name') # TODO CHANGE NAME of table to history? and history_actor ... etc
history_actor_table = ConnectiveTable(HistoryActor, 'history_actor', history_table, actor_table)
history_location_table = ConnectiveTable(HistoryLocation, 'history_location', history_table, location_table)
history_faction_table = ConnectiveTable(HistoryFaction, 'history_faction', history_table, faction_table)

object_table = QueryableTable(Object_, 'object_', 'object_id', 'object_name')
history_object_table = ConnectiveTable(HistoryObject, 'history_object', object_table, history_table)
object_to_owner_table = ConnectiveTable(ObjectToOwner, 'object_to_owner', object_table, actor_table)

world_data_table = QueryableTable(WorldData, 'world_data', 'world_data_id', 'data_name')
history_world_data_table = ConnectiveTable(HistoryWorldData, 'history_world_data', history_table, world_data_table)

# Here we connect up the tables

actor_table.connect_to_endcaps([class_table, background_table, race_table, sub_race_table])
actor_table.connect_to_connective_tables([faction_members_table, residents_table, history_actor_table])



faction_table.connect_to_connective_tables([faction_members_table, location_to_faction_table, history_table])
faction_table.connect_to_self_connective_tables([faction_a_on_b_relations_table])

location_table.connect_to_endcaps([location_city_table])
location_table.connect_to_connective_tables([location_to_faction_table, residents_table, history_location_table])

history_table.connect_to_endcaps([])
history_table.connect_to_connective_tables([history_actor_table, history_faction_table, history_location_table, history_object_table, history_world_data_table])

object_table.connect_to_endcaps([])
object_table.connect_to_connective_tables([history_object_table, object_to_owner_table])

world_data_table.connect_to_endcaps([])
world_data_table.connect_to_connective_tables([history_world_data_table])