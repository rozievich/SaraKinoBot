import psycopg2
from psycopg2.extras import DictCursor


conn = psycopg2.connect(
    user="postgres",
    dbname="sara_db",
    password="black0613",
    host="localhost",
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
        username VARCHAR(128) NOT NULL,
        channel_id VARCHAR(128) UNIQUE,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    media_query = '''
    CREATE TABLE IF NOT EXISTS movies(
        id BIGSERIAL PRIMARY KEY,
        post_id INT NOT NULL,
        file_id VARCHAR(800) NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT now()
    )
    '''
    cur.execute(query)
    cur.execute(channel_query)
    cur.execute(media_query)
    conn.commit()
