from app.db import Base, engine
from app.models import Link, ClickEvent  # important: registers models
Base.metadata.create_all(bind=engine)
print("Tables created successfully")