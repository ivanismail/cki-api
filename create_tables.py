#!/usr/bin/env python
"""Script to create all database tables"""

import os
from dotenv import load_dotenv

load_dotenv()

# Print connection info for debugging
print("Database Configuration:")
print(f"  DB_HOST: {os.getenv('DB_HOST')}")
print(f"  DB_PORT: {os.getenv('DB_PORT')}")
print(f"  DB_USER: {os.getenv('DB_USER')}")
print(f"  DB_NAME: {os.getenv('DB_NAME')}")

from app.database import engine, Base, SQLALCHEMY_DATABASE_URL
from app import models

print(f"\nConnection String: {SQLALCHEMY_DATABASE_URL}")

if __name__ == "__main__":
    print("\nCreating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully!")
        print("\nTables created:")
        for table in Base.metadata.tables:
            print(f"  - {table}")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        import traceback
        traceback.print_exc()
