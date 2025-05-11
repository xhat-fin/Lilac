import os
from psycopg2 import connect, sql
from dotenv import load_dotenv
from datetime import datetime

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

                
                CREATE TABLE IF NOT EXISTS reflections (
                    id SERIAL PRIMARY KEY,
                    plant_id INTEGER REFERENCES plants(id) ON DELETE CASCADE,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL
                );
            """
        )

# получение всех кустов
def get_all_plants():
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT id, name, type, planted_by, growth_stage FROM plants ORDER BY id;
            """)
        plants = cur.fetchall()
    return plants


def plant(name, ptype, planted_by):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute('''
                INSERT INTO plants (name, type, planted_by, growth_stage, last_watered, created_at)
                VALUES (%s, %s, %s, 0, %s, %s)
            ''', (name, ptype, planted_by, datetime.now(), datetime.now()))
        conn.commit()


def insert_quest(plant_id, question, answer):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO reflections (plant_id, question, answer, created_at)
            VALUES (%s, %s, %s, %s)
        """, (plant_id, question, answer, datetime.now()))
        conn.commit()


def update_stage(id):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE plants
            SET last_watered = %s,
                growth_stage = growth_stage + 1
            WHERE id = %s
            """, (datetime.now(), id))
        conn.commit()


def delete_plant(id):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""
        DELETE FROM plants WHERE id = %s
        """, (id,))
        conn.commit()


def get_reflections(plant_id):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT question, answer, created_at
            FROM reflections
            WHERE plant_id = %s
            ORDER BY created_at DESC
        """, (plant_id,))
        return cur.fetchall()


def get_plant(id):
    with get_db_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM plants WHERE id = %s", (id,))
        return cur.fetchone()


init_db()
