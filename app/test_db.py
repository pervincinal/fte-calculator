import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+pg8000://test:Pervin21@34.147.188.76:5432/postgres")

try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("Database connected successfully!")
    conn.close()
except Exception as e:
    print(f"Database connection failed: {e}")
