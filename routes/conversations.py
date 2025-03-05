from fastapi import APIRouter
from database import get_db_connection
from models import ConversationCreate

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
