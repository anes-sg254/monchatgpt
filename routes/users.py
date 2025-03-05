from fastapi import APIRouter, Depends
from database import get_db_connection
from models import UserCreate, UserOut
import bcrypt

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    conn = get_db_connection()
    if not conn:
        return {"error": "Connexion à la base impossible"}

    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id, username, email, created_at",
                (user.username, user.email, hashed_password),
            )
            new_user = cursor.fetchone()
            conn.commit()
        return new_user
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
