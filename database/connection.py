from pathlib import Path

database_dir = Path("/content/database")
database_dir.mkdir(parents=True, exist_ok=True)

(database_dir / "__init__.py").touch(exist_ok=True)

print("SUCCESS: Database directory created!")
print("/content/database/")

connection_code = '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from backend.config import settings

DATABASE_URL = settings.database_url

# SQLite configuration
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }

# Database engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False
)

# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for database models
class Base(DeclarativeBase):
    pass

# Database dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Database connection test
def check_database_connection():
    from sqlalchemy import text

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return True
'''

path = Path("/content/database/connection.py")
path.write_text(connection_code, encoding="utf-8")

print("SUCCESS: connection.py created!")
