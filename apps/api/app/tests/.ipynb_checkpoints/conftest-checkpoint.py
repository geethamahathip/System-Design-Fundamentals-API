import pytest
from fastapi.testclient import TestClient
from apps.api.app.main import app
from app.db import Base, engine, SessionLocal

@pytest.fixture(scope="session")
def client():
    Base.metadata.create_all(bind=engine)
    return TestClient(app)


@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()