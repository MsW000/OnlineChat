from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .db import get_db, Base, engine

app = FastAPI(title="OnlineChat", version="1.0")

@app.get("/")
def root(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except:
        db_status = "disconnected"
    
    return {
        "message": "OnlineChat API работает!",
        "database": db_status,
        "docs": "/docs"
    }

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {"status": "ok", "service": "onlinechat"}

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("FastAPI запущен, таблицы созданы")

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": len(users)}