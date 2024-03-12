import csv, os
import psycopg2 as pg
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('CONNSTR')

def open_csv_and_query(query:str, file_location:str, cursor:pg.extensions.cursor):
    with open(file_location) as f:
        values = csv.reader(f)
        headers = next(values)
        
        for i in values:
            cursor.execute(query, i)

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

class_table = Pg_Table("class")
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
historical_fragment_table = Pg_Table('historical_fragment')
involved_history_actor_table = Pg_Table('involved_history_actor')
involved_history_location_table = Pg_Table('involved_history_location')
object_table = Pg_Table('object_')
involved_history_object_table = Pg_Table('involved_history_object')
world_data_table = Pg_Table('world_data')
involved_history_world_data_table = Pg_Table('involved_history_world_data')


