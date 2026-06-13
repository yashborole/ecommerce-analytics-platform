from app import models, schemas
from app.database import SessionLocal

def create_user(user: schemas.UserCreate):
    try:
        db = SessionLocal()
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        return {"error": str(e)}

def get_users():
    try:
        db = SessionLocal()
        return db.query(models.User).all()
    except Exception as e:
        return {"error": str(e)}

def get_user_by_id(user_id: int):
    try:
        db = SessionLocal()
        return db.query(models.User).filter(models.User.id == user_id).first()
    except Exception as e:
        return {"error": str(e)}

def login(user_name: str, password: str):
    try:
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.name == user_name).first()
        if not user:
            return {"error": "Invalid username or password"}
        return {"message": "Login successful", "user_id": user.id, "name": user.name}
    except Exception as e:
        return {"error": str(e)}
