from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# 1. Загружаем .env (он в папке backend)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# 2. Берём URL из .env или используем по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:zero42@localhost:5432/postgres")

# 3. Создаём "движок" (подключение к БД)
engine = create_engine(DATABASE_URL)

# 4. Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Базовый класс для всех моделей
Base = declarative_base()

# 6. Функция для получения сессии (используется в Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db  # Отдаём сессию FastAPI
    finally:
        db.close()  # Закрываем после использования