from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

# Базовый класс для всех моделей
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age})>"

# Экспортируем Base для Alembic
__all__ = ['Base', 'User']