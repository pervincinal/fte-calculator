from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ftecalc_user:FTECalc2024!@34.147.188.76:5432/ftecalc")

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models
from . import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QA FTE Calculator API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "QA FTE Calculator API", "version": "1.0.0"}

# Import the routes from main_simple.py manually
# Since your app is probably working with main_simple.py, 
# let's just use that directly
