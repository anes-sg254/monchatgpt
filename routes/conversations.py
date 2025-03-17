from fastapi import APIRouter
from database import get_db_connection
from models import ConversationCreate
from typing import List
import psycopg2

router = APIRouter()

@router.post("/")
def create_conversation(conversation: ConversationCreate):
    conn = get_db_connection()
    if not conn:
        return {"error": "Connexion à la base impossible"}

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Conversations (user_id) VALUES (%s) RETURNING id, created_at",
                (conversation.user_id,),
            )
            new_conversation = cursor.fetchone()
            conn.commit()
        return new_conversation
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()


@router.get("/{user_id}")
def get_user_conversations(user_id: int):
    conn = get_db_connection()
    if not conn:
        return {"error": "Connexion à la base impossible"}

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, user_id, created_at FROM Conversations WHERE user_id = %s ORDER BY created_at DESC",
                (user_id,),
            )
            conversations = cursor.fetchall()
            print("Résultats SQL :", conversations) 

        if not conversations:
            return {"error": "Aucune conversation trouvée pour cet utilisateur"}

        return conversations
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

