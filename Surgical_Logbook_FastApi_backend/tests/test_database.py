from sqlmodel import SQLModel,create_engine,Session
from config import settings
from models import *

# isolated database for testing
test_engine = create_engine(settings.test_database_url)

# inherits models schemas and create tables no alembic
SQLModel.metadata.create_all(test_engine)

# tests dependency
def get_session():
    """Yield a session for testing. Each test can override dependency."""
    with Session(test_engine) as session:
        yield session