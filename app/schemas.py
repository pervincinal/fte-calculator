from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TribeBase(BaseModel):
    name: str
    priority: str
    chapter_lead_id: Optional[int] = None

class TribeCreate(TribeBase):
    pass

class TribeUpdate(TribeBase):
    pass

class Tribe(TribeBase):
    id: int
    class Config:
        orm_mode = True

class SquadBase(BaseModel):
    name: str
    tribe_id: int
    priority: str
    status: str = "ACTIVE"
    platforms: List[str] = []

class SquadCreate(SquadBase):
    pass

class SquadUpdate(SquadBase):
    last_calculation: Optional[Dict[str, Any]] = None

class Squad(SquadBase):
    id: int
    class Config:
        orm_mode = True

class ChapterLeadBase(BaseModel):
    name: str
    email: Optional[str] = None

class ChapterLeadCreate(ChapterLeadBase):
    pass

class ChapterLeadUpdate(ChapterLeadBase):
    pass

class ChapterLead(ChapterLeadBase):
    id: int
    class Config:
        orm_mode = True

class CalculateRequest(BaseModel):
    squad_id: Optional[int] = None
    DEV_COUNT: int = 0
    STORIES_PER_SPRINT: int = 0
    CURR_L1: int = 0
    CURR_L2: int = 0
    CURR_L3: int = 0
    CURR_L4: int = 0
    CURR_L5: int = 0
    SHARED_AUTO_FTE: float = 0
    SHARED_PERF_FTE: float = 0

class CalculationResult(BaseModel):
    needed_fte: float
    current_fte: float
    fte_gap: float
    gap_risk_level: str
    confidence_score: int

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
