import psycopg2
from psycopg2.extras import RealDictCursor

# Paramètres de connexion
DATABASE_CONFIG = {
    "host": "localhost",
    "dbname": "chatgpt",
    "user": "postgres",
    "password": "msprepsi",
    "port": "5432",
}

# Fonction pour se connecter à PostgreSQL
def get_db_connection():
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None
