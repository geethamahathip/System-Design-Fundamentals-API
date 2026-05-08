from app.db import SessionLocal
from app.auth import get_principal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()