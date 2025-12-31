from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

# Импортируем зависимые файлы
from .db import get_db, Base, engine
from .models import User, Message

app = FastAPI(title="OnlineChat", version="1.0")

# При старте создаём таблицы в БД
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы в БД")

@app.get("/")
def root():
    return {"message": "OnlineChat API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

# 1. ПОЛУЧЕНИЕ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    """
    Аналог SQL: SELECT * FROM users
    """
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "age": u.age} for u in users]

# 2. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
@app.post("/users")
def create_user(name: str, age: int, db: Session = Depends(get_db)):
    """
    Аналог SQL: INSERT INTO users (name, age) VALUES (name, age)
    """
    user = User(name=name, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "message": "Пользователь создан",
        "user": {"id": user.id, "name": user.name, "age": user.age}
    }

# 3. ПОЛУЧЕНИЕ СООБЩЕНИЙ
@app.get("/messages")
def get_messages(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Если user_id указан: SELECT * FROM messages WHERE user_id = ...
    Если не указан: SELECT * FROM messages
    """
    query = db.query(Message)
    
    if user_id:
        query = query.filter(Message.user_id == user_id)
    
    messages = query.order_by(Message.created_at.desc()).all()
    
    return [
        {
            "id": msg.id,
            "text": msg.text,
            "user_id": msg.user_id,
            "created_at": msg.created_at.isoformat(),
            "user_name": msg.user.name  # Берём имя из связанной таблицы
        }
        for msg in messages
    ]

# 4. ОТПРАВКА СООБЩЕНИЯ
@app.post("/messages")
def create_message(text: str, user_id: int, db: Session = Depends(get_db)):
    # Проверяем есть ли пользователь
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Создаём сообщение
    message = Message(text=text, user_id=user_id)
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "message": "Сообщение отправлено",
        "id": message.id,
        "text": message.text,
        "user_id": message.user_id,
        "created_at": message.created_at.isoformat()
    }