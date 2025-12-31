from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# Импортируем Base из db.py
from .db import Base

class User(Base):
    __tablename__ = "users"  # Имя таблицы в БД
    
    # Столбцы таблицы (как в SQL)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # NOT NULL
    age = Column(Integer, nullable=False)   # NOT NULL
    
    # Связь с сообщениями (пока просто знай что это есть)
    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с users.id
    created_at = Column(DateTime, default=datetime.utcnow)  # Автоматическая дата
    
    # Обратная связь
    user = relationship("User", back_populates="messages")