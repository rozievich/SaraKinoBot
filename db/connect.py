import psycopg2
from os import getenv
from dotenv import load_dotenv
from psycopg2.extras import DictCursor

load_dotenv(".env")

conn = psycopg2.connect(
    user="postgres",
    dbname=getenv('DB_NAME'),
    password=getenv('PASSWORD'),
    host=getenv('HOST'),
    port=5432,
    cursor_factory=DictCursor
)
cur = conn.cursor()


def startup_table():
    query = '''
    CREATE TABLE IF NOT EXISTS users(
        id BIGSERIAL PRIMARY KEY,
        telegram_id VARCHAR(60) UNIQUE,
        created_at TIMESTAMP DEFAULT now()
        )
    '''
    channel_query = '''
    CREATE TABLE IF NOT EXISTS channels(
        id BIGSERIAL PRIMARY KEY,
        username VARCHAR(32) UNIQUE,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    media_query = '''
    CREATE TABLE IF NOT EXISTS movies(
        id BIGSERIAL PRIMARY KEY,
        post_id BIGSERIAL NOT NULL,
        file_id VARCHAR(800) NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    cur.execute(query)
    cur.execute(channel_query)
    cur.execute(media_query)
    conn.commit()
