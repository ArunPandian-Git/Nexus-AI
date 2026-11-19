%%writefile /content/database/init_db.py

from database.connection import engine, Base
from database import models

def init_database():
    print("NEXUS AI DATABASE INITIALIZATION")
    print("=" * 45)

    try:
        Base.metadata.create_all(bind=engine)

        print("SUCCESS: DATABASE TABLES CREATED!")

        for table_name in Base.metadata.tables:
            print(f"TABLE CREATED: {table_name}")

        print(f"\nTOTAL TABLES: {len(Base.metadata.tables)}")
        print("DATABASE INITIALIZATION COMPLETED!")

        return True

    except Exception as error:
        print("DATABASE INITIALIZATION FAILED!")
        print("ERROR:", error)
        return False

  from database.init_db import init_database

init_database()

from sqlalchemy import inspect
from database.connection import engine

inspector = inspect(engine)

tables = inspector.get_table_names()

print("DATABASE TABLE VERIFICATION")
print("=" * 45)

for table in tables:
    print("VERIFIED:", table)

print("\nTOTAL VERIFIED TABLES:", len(tables))

assert len(tables) == 5, "Expected exactly 5 database tables!"

print("\nSUCCESS: ALL DATABASE TABLES VERIFIED!")
