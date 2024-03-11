DROP TABLE IF EXISTS class, background, race, sub_race, actor, skills, actor_to_skills, faction, faction_a_on_b_relations, faction_members, location_, location_to_faction, location_dungeon, location_city, location_city_districts, residents, location_flora_fauna, historical_fragments, involved_history_actor, involved_history_location, involved_history_faction, object_, involved_history_object, object_to_owner, world_data, involved_history_world_data CASCADE;


CREATE TABLE class(
    id SERIAL PRIMARY KEY,
    class_name VARCHAR(255),
    class_description TEXT
);

CREATE TABLE background(
    id SERIAL PRIMARY KEY,
    background_name VARCHAR(255),
    background_description TEXT
);

CREATE TABLE race(
    id SERIAL PRIMARY KEY,
    race_name VARCHAR(255),
    race_description TEXT
);

CREATE TABLE sub_race(
    id SERIAL PRIMARY KEY,
    parent_race_id INT,
    sub_race_name VARCHAR(255),
    sub_race_description TEXT,

    FOREIGN KEY (parent_race_id) REFERENCES race(id)
);

CREATE TABLE actor(
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    title TEXT,
    actor_age INT,
    class_id INT,
    actor_level INT,
    background_id INT,
    job TEXT,
    actor_role TEXT,
    race_id INT,
    sub_race_id INT,
    alignment VARCHAR(2),
    strength INT,
    dexterity INT,
    constitution INT,
    intelligence INT,
    wisdom INT,
    charisma INT,
    ideal TEXT,
    bond TEXT,
    flaw TEXT,
    appearance TEXT,
    strengths TEXT,
    weaknesses TEXT,
    notes TEXT,

    FOREIGN KEY (class_id) REFERENCES class(id),
    FOREIGN KEY (background_id) REFERENCES background(id),
    FOREIGN KEY (race_id) REFERENCES race(id),
    FOREIGN KEY (sub_race_id) REFERENCES sub_race(id)
);

CREATE TABLE skills(
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(255),
    skill_description TEXT,
    skill_trait VARCHAR(255)
);

CREATE TABLE actor_to_skills(
    id SERIAL PRIMARY KEY,
    actor_id INT,
    skill_id INT,
    skill_level INT,

    FOREIGN KEY (actor_id) REFERENCES actor(ID),
    FOREIGN KEY (skill_id) REFERENCES skills(ID)
);

CREATE TABLE faction(
    id SERIAL PRIMARY KEY,
    faction_name VARCHAR(255),
    faction_description TEXT,
    goals TEXT,
    faction_values TEXT,
    faction_income_sources TEXT,
    faction_expenses TEXT
);

CREATE TABLE faction_a_on_b_relations(
    id SERIAL PRIMARY KEY,
    faction_a_id INT,
    faction_b_id INT,
    overall TEXT,
    economically TEXT,
    politically TEXT,
    opinion TEXT,

    FOREIGN KEY (faction_a_id) REFERENCES faction(id),
    FOREIGN KEY (faction_b_id) REFERENCES faction(id)
);

CREATE TABLE faction_members(
    id SERIAL PRIMARY KEY,
    actor_id INT,
    faction_id INT,
    actor_role VARCHAR(255),
    relative_power INT,

    FOREIGN KEY (actor_id) REFERENCES actor(ID),
    FOREIGN KEY (faction_id) REFERENCES faction(ID)
);

CREATE TABLE location_(
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(255),
    location_type VARCHAR(255),
    location_description TEXT,
    sights TEXT,
    smells TEXT,
    sounds TEXT,
    feels TEXT,
    tastes TEXT,
    coordinates VARCHAR(255)
);

CREATE TABLE location_to_faction(
    id SERIAL PRIMARY KEY,
    location_id INT,
    faction_id INT,
    faction_presence FLOAT,
    faction_power FLOAT,
    notes TEXT,

    FOREIGN KEY (location_id) REFERENCES location_(id),
    FOREIGN KEY (faction_id) REFERENCES faction(id)
);

CREATE TABLE location_dungeon(
    id SERIAL PRIMARY KEY,
    location_id INT,
    dangers TEXT,
    traps TEXT,
    secrets TEXT,

    FOREIGN KEY (location_id) REFERENCES location_(id)
);

CREATE TABLE location_city(
    id SERIAL PRIMARY KEY,
    location_id INT, 
    government TEXT,
    
    FOREIGN KEY (location_id) REFERENCES location_(id)
);

CREATE TABLE location_city_districts(
    id SERIAL PRIMARY KEY,
    location_id INT,
    district_id INT,

    FOREIGN KEY (location_id) REFERENCES location_(id),
    FOREIGN KEY (district_id) REFERENCES location_(id)
);

CREATE TABLE residents(
    id SERIAL PRIMARY KEY,
    actor_id INT,
    location_id INT,

    FOREIGN KEY (actor_id) REFERENCES actor(id),
    FOREIGN KEY (location_id) REFERENCES location_(id)
);

CREATE TABLE location_flora_fauna(
    id SERIAL PRIMARY KEY,
    location_id INT,
    living_name VARCHAR(255),
    living_description TEXT,
    living_type TEXT,

    FOREIGN KEY (location_id) REFERENCES location_(id)
);

CREATE TABLE historical_fragments(
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255),
    event_year INT,
    event_description TEXT
);

CREATE TABLE involved_history_actor(
    id SERIAL PRIMARY KEY,
    historical_fragment_id INT,
    actor_id INT,

    FOREIGN KEY (historical_fragment_id) REFERENCES historical_fragments(id),
    FOREIGN KEY (actor_id) REFERENCES actor(id)
);

CREATE TABLE involved_history_location(
    id SERIAL PRIMARY KEY,
    historical_fragment_id INT,
    location_id INT,

    FOREIGN KEY (historical_fragment_id) REFERENCES historical_fragments(id),
    FOREIGN KEY (location_id) REFERENCES location_(id)
);

CREATE TABLE involved_history_faction(
    id SERIAL PRIMARY KEY,
    historical_fragment_id INT,
    faction_id INT,
    
    FOREIGN KEY (historical_fragment_id) REFERENCES historical_fragments(id),
    FOREIGN KEY (faction_id) REFERENCES faction(id)
);

CREATE TABLE object_(
    id SERIAL PRIMARY KEY,
    object_name VARCHAR(255),
    object_description TEXT,
    object_value INT,
    rarity VARCHAR(255)
);

CREATE TABLE involved_history_object(
    id SERIAL PRIMARY KEY,
    historical_fragment_id INT,
    object_id INT,

    FOREIGN KEY (historical_fragment_id) REFERENCES historical_fragments(id),
    FOREIGN KEY (object_id) REFERENCES object_(id)
);

CREATE TABLE object_to_owner(
    id SERIAL PRIMARY KEY,
    object_id INT,
    actor_id INT,

    FOREIGN KEY (object_id) REFERENCES object_(id),
    FOREIGN KEY (actor_id) REFERENCES actor(id)
);

CREATE TABLE world_data(
    id SERIAL PRIMARY KEY,
    data_name VARCHAR(255),
    data_description TEXT
);

CREATE TABLE involved_history_world_data(
    id SERIAL PRIMARY KEY,
    historical_fragment_id INT,
    world_data_id INT,

    FOREIGN KEY (historical_fragment_id) REFERENCES historical_fragments(id),
    FOREIGN KEY (world_data_id) REFERENCES world_data(id)
);