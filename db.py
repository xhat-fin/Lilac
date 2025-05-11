import os
from psycopg2 import connect, sql
from dotenv import load_dotenv
load_dotenv()

# Конфигурация базы данных
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')



def get_db_connection():
    return connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def init_db():
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS plants (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    planted_by TEXT,
                    growth_stage INTEGER DEFAULT 0,
                    last_watered TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS actions (
                    id SERIAL PRIMARY KEY,
                    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
                    action_type TEXT NOT NULL, -- 'plant', 'water', 'fertilize'
                    actor_name TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS reflections (
                    id SERIAL PRIMARY KEY,
                    bush_id INTEGER REFERENCES plants(id),
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
            """
        )

init_db()
