from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from typing import List

from db_models import User, Base

# Создаём FastAPI приложение
app = FastAPI(title="OnlineChat API", version="1.0.0")

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:zerol02@localhost:5432/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Событие при запуске приложения
@app.on_event("startup")
def startup():
    # Создаём таблицы если их нет (для разработки)
    Base.metadata.create_all(bind=engine)
    print("✅ База данных подключена!")

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в OnlineChat API!", "status": "работает!"}

# Получить всех пользователей
@app.get("/users", response_model=List[dict])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {"id": user.id, "name": user.name, "age": user.age}
        for user in users
    ]

# Создать нового пользователя
@app.post("/users")
def create_user(name: str, age: int, db: Session = Depends(get_db)):
    user = User(name=name, age=age)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Пользователь создан", "user": {"id": user.id, "name": user.name, "age": user.age}}

# Проверка здоровья
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "onlinechat-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)