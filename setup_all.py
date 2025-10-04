import os
from pathlib import Path

# Create directory structure
dirs = [
    "app/api/endpoints",
    "app/models",
    "app/schemas",
    "app/services",
    "app/db"
]

for dir_path in dirs:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    (Path(dir_path) / "__init__.py").touch()

# Create all files
files = {
    "app/main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="QA FTE Calculator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "QA FTE Calculator API"}

@app.post("/api/v1/calculate")
def calculate(data: dict):
    return {
        "needed_fte": 4.5,
        "current_fte": 3.0,
        "gap": 1.5
    }
''',

    "app/db/database.py": '''from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./qafte.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
''',

    "app/models/models.py": '''from sqlalchemy import Column, Integer, String, Float, JSON
from app.db.database import Base

class Squad(Base):
    __tablename__ = "squads"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tribe_id = Column(Integer)

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True)
    squad_id = Column(Integer)
    needed_fte = Column(Float)
    current_fte = Column(Float)
    gap = Column(Float)
    inputs = Column(JSON)
'''
}

for file_path, content in files.items():
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created {file_path}")

print("\n🎉 Setup complete!")