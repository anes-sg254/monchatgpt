from fastapi import APIRouter
from database import get_db_connection
from models import MessageCreate
from services.ai_service import get_ai_response
from typing import List
import psycopg2.extras

router = APIRouter()
@router.post("/chat")
def chat_with_ai(message: MessageCreate):
    print("🔥 Route TEST appelée avec :", message.content)
    ai_response = get_ai_response(message.content)
    print("🟢 Réponse IA générée :", ai_response)  
    return {"user_message": message.content, "ai_response": ai_response}

@router.post("/")
def add_message(message: MessageCreate):
    conn = get_db_connection()
    if not conn:
        return {"error": "Connexion à la base impossible"}

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Messages (conversation_id, sender, content) VALUES (%s, %s, %s) RETURNING id, created_at",
                (message.conversation_id, message.sender, message.content),
            )
            new_message = cursor.fetchone()
            conn.commit()
        return new_message
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

@router.get("/{conversation_id}")
def get_messages(conversation_id: int):
    conn = get_db_connection()
    if not conn:
        return {"error": "Connexion à la base impossible"}

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(
                "SELECT id, sender, content, created_at FROM Messages WHERE conversation_id = %s ORDER BY created_at ASC",
                (conversation_id,),
            )
            messages = cursor.fetchall()
            print("Résultats SQL :", messages)  

        if not messages:
            return {"error": "Aucun message trouvé pour cette conversation"}

        return messages  
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()




