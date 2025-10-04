from pydantic import BaseModel

class CalculationResult(BaseModel):
    needed_fte: float
    current_fte: float
    fte_gap: float
    gap_risk_level: str
    confidence_score: int

def calculate_fte(inputs: dict) -> CalculationResult:
    """Calculate FTE requirements based on inputs"""
    
    # Base FTE calculation
    dev_count = inputs.get('DEV_COUNT', 0)
    stories = inputs.get('STORIES_PER_SPRINT', 0)
    
    # Start with a base requirement
    base_fte = 1.5
    
    # Add based on team size and workload
    base_fte += (dev_count * 0.15)
    base_fte += (stories * 0.05)
    
    # The NEEDED FTE is what the squad actually requires
    needed_fte = base_fte
    
    # Calculate current team capacity
    current_capacity = (
        inputs.get('CURR_L1', 0) * 0.3 +
        inputs.get('CURR_L2', 0) * 0.5 +
        inputs.get('CURR_L3', 0) * 0.7 +
        inputs.get('CURR_L4', 0) * 0.9 +
        inputs.get('CURR_L5', 0) * 1.0
    )
    
    # Shared support ADDS to current capacity (max 0.5 FTE each)
    shared_auto_fte = min(float(inputs.get('SHARED_AUTO_FTE', 0)), 0.5)
    shared_perf_fte = min(float(inputs.get('SHARED_PERF_FTE', 0)), 0.5)
    
    # Total current FTE
    current_fte = current_capacity + shared_auto_fte + shared_perf_fte
    
    # Gap is what's missing
    fte_gap = max(0, needed_fte - current_fte)
    
    # Determine risk level
    if fte_gap >= 2.5:
        gap_risk_level = "CRITICAL"
    elif fte_gap >= 1.5:
        gap_risk_level = "HIGH"
    elif fte_gap >= 0.5:
        gap_risk_level = "MEDIUM"
    elif fte_gap > 0:
        gap_risk_level = "LOW"
    else:
        gap_risk_level = "NO RISK"
    
    return CalculationResult(
        needed_fte=round(needed_fte, 2),
        current_fte=round(current_fte, 2),
        fte_gap=round(fte_gap, 2),
        gap_risk_level=gap_risk_level,
        confidence_score=100
    )
