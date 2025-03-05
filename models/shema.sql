from config_db import connect_to_db


def create_users_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Table Users vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table Users : {e}")


def create_conversations_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Conversations (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Table Conversations vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table Conversations : {e}")

def create_messages_table(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INTEGER REFERENCES Conversations(id) ON DELETE CASCADE,
                    sender VARCHAR(10) CHECK (sender IN ('user', 'model')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            print("Table Messages vérifiée/créée avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création de la table Messages : {e}")


def main():
    # Connexion à la base de données
    conn = connect_to_db()
    if conn:
        create_users_table(conn)
        create_conversations_table(conn)
        create_messages_table(conn)

        # Fermer la connexion
        conn.close()
        print("Connexion à la base de données fermée.")

if __name__ == "__main__":
    main()
