import psycopg2 as pg
# import utils
import os, csv
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')

def main():
    conn = pg.connect(db_url)
    curs = conn.cursor()
    with open('db/seed.sql', 'r') as f:
        seed_query = f.read()
        curs.execute(seed_query)
    # answer = cur.fetchall()
    # print(answer)
    # cur.execute()

    # utils.open_csv_and_query(utils.class_table.build_query(), 'db/classes.csv', curs)
    # utils.open_csv_and_query(utils.background_table.build_query(), 'db/backgrounds.csv', curs)
    # utils.open_csv_and_query(utils.race_table.build_query(), 'db/races.csv', curs)
    # utils.open_csv_and_query(utils.sub_race_table.build_query(), 'db/sub_races.csv', curs)
    # utils.open_csv_and_query(utils.actor_table.build_query(), 'db/actors.csv', curs)

    
    conn.commit()
    curs.close()
    conn.close()


if __name__ == "__main__":
    main()