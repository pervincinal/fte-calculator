from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# Your password needs proper URL encoding
password = urllib.parse.quote_plus("Pervin21@")

# Use the default 'postgres' database that already exists
SQLALCHEMY_DATABASE_URL = f"postgresql+pg8000://test:{password}@34.147.188.76:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()