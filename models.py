from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

class ConversationCreate(BaseModel):
    user_id: int

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str
