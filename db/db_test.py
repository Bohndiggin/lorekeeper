import psycopg2 as pg
import utils
import os, seed
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')

def main():
    conn = pg.connect(db_url)
    cur = conn.cursor()

    with open('db/seed.sql', 'r') as f:
        seed_query = f.read()
        cur.execute(seed_query)

    utils.open_csv_and_query(utils.class_table.build_query(), 'db/classes.csv', cur)
    utils.open_csv_and_query(utils.background_table.build_query(), 'db/backgrounds.csv', cur)
    utils.open_csv_and_query(utils.race_table.build_query(), 'db/races.csv', cur)
    utils.open_csv_and_query(utils.sub_race_table.build_query(), 'db/sub_races.csv', cur)

    utils.open_csv_and_query(utils.actor_table.build_query(), "db/test_data/actors_test.csv", cur)
    
    utils.open_csv_and_query(utils.faction_table.build_query(),"db/test_data/factions_test.csv", cur)

    utils.open_csv_and_query(utils.faction_a_on_b_relations_table.build_query(), "db/test_data/faction_relations_test.csv", cur)

    utils.open_csv_and_query(utils.faction_members_table.build_query(), "db/test_data/faction_members_test.csv", cur)

    utils.open_csv_and_query(utils.location_table.build_query(), 'db/test_data/location_test.csv', cur)
    utils.open_csv_and_query(utils.location_to_faction_table.build_query(), 'db/test_data/location_to_faction_test.csv', cur)
    utils.open_csv_and_query(utils.location_dungeon_table.build_query(), 'db/test_data/location_dungeon_test.csv', cur)
    utils.open_csv_and_query(utils.location_city_table.build_query(), 'db/test_data/location_city_test.csv', cur)
    utils.open_csv_and_query(utils.location_city_districts_table.build_query(), 'db/test_data/location_city_districts_test.csv', cur)
    utils.open_csv_and_query(utils.residents_table.build_query(), 'db/test_data/residents_test.csv', cur)
    utils.open_csv_and_query(utils.history_table.build_query(), 'db/test_data/historical_fragments_test.csv', cur)
    utils.open_csv_and_query(utils.history_actor_table.build_query(), 'db/test_data/involved_history_actor_test.csv', cur)
    utils.open_csv_and_query(utils.history_location_table.build_query(), 'db/test_data/involved_history_location_test.csv', cur)
    utils.open_csv_and_query(utils.object_table.build_query(), 'db/test_data/object_test.csv', cur)
    utils.open_csv_and_query(utils.history_object_table.build_query(), 'db/test_data/involved_history_object_test.csv', cur)
    utils.open_csv_and_query(utils.world_data_table.build_query(), 'db/test_data/world_data_test.csv', cur)
    utils.open_csv_and_query(utils.history_world_data_table.build_query(), 'db/test_data/involved_history_world_data_test.csv', cur)



    conn.commit()
    cur.close()
    conn.close()





if __name__ == "__main__":
    seed.main()
    main()