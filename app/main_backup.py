from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "QA FTE Calculator API is running"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

# Mock endpoints for testing
@app.get("/api/v1/tribes")
def get_tribes():
    return {"items": [{"id": 1, "name": "CDX", "priority": "HIGH"}]}

@app.get("/api/v1/squads")
def get_squads():
    return {"items": [{"id": 1, "name": "Personal Cabinet", "tribe_id": 1}]}
