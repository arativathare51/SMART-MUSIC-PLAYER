#database
import mysql.connector
from contextlib import contextmanager#this lib is used to create safe database connection that automatically closes

@contextmanager
def db_connection():
    #Safely manages database connections (auto-closes them)
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="*******",
            database="music_player"
        )
        yield conn
    except mysql.connector.Error as err:
        print(f"⚠️ Database Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_songs():
    """Fetches all songs from the database."""
    with db_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT song_name, song_path FROM songs")
            return cursor.fetchall()#fetch all rows(songs) from the table and return them
    return []#if connection fails it returns empty list

def get_song_id(song_path):
    """Fetches song ID from the database."""
    with db_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT song_id FROM songs WHERE song_path = %s", (song_path,))
            result = cursor.fetchone()#fetch only one row
            return result[0] if result else None#if found, return song id
    return None

def insert_play_history(song_id):
    """Records a song play in the database."""
    with db_connection() as conn:
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO play_history (song_id, play_time) VALUES (%s, NOW())", (song_id,))
            conn.commit()#save changes permanantly in database 
