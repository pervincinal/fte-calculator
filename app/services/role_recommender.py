from typing import Dict, Tuple, Optional, List
from sqlalchemy.orm import Session

NO_RISK_THRESHOLD = 0.50

def classify_risk(gap: float) -> str:
    """Classify risk based on FTE gap"""
    if gap < NO_RISK_THRESHOLD:
        return "NONE"
    if gap < 1.0:
        return "LOW"
    if gap < 2.0:
        return "MEDIUM"
    return "HIGH"

def load_policy(db: Session) -> Dict:
    """Load recommended mix policy from database"""
    # For now, return default policy
    return {
        "DEFAULT": {
            "CRITICAL": {"L5": 0.15, "L4": 0.25, "L3": 0.35, "L2": 0.20, "L1": 0.05},
            "HIGH": {"L5": 0.10, "L4": 0.20, "L3": 0.40, "L2": 0.25, "L1": 0.05},
            "MEDIUM": {"L5": 0.05, "L4": 0.15, "L3": 0.40, "L2": 0.30, "L1": 0.10},
            "LOW": {"L5": 0.00, "L4": 0.10, "L3": 0.35, "L2": 0.35, "L1": 0.20}
        },
        "PLATFORM_TWEAKS": {
            "API_HEAVY": {"L4": 0.05, "L3": 0.05, "L2": -0.05, "L1": -0.05},
            "MOBILE_HEAVY": {"L3": 0.05, "L2": 0.05, "L1": -0.10}
        }
    }

def load_constraints(priority: str, db: Session) -> Dict:
    """Load level constraints for given priority"""
    defaults = {
        "CRITICAL": {"minSeniorShare": 0.40, "maxJuniorShare": 0.25},
        "HIGH": {"minSeniorShare": 0.30, "maxJuniorShare": 0.35},
        "MEDIUM": {"minSeniorShare": 0.20, "maxJuniorShare": 0.45},
        "LOW": {"minSeniorShare": 0.10, "maxJuniorShare": 0.55}
    }
    return defaults.get(priority, {"minSeniorShare": 0, "maxJuniorShare": 1.0})

def build_target_share(priority: str, platforms: List[str], custom: Optional[Dict], db: Session) -> Dict:
    """Build target share distribution based on priority and platforms"""
    policy = load_policy(db)

    # Start with base priority mix
    target = dict(policy["DEFAULT"].get(priority, {}))

    # Apply platform tweaks
    if platforms:
        if "API" in platforms and not any(p in platforms for p in ["ANDROID", "IOS"]):
            tweaks = policy.get("PLATFORM_TWEAKS", {}).get("API_HEAVY", {})
            for level, delta in tweaks.items():
                if level in target:
                    target[level] = max(0.0, target[level] + delta)

    # Override with custom if provided
    if custom:
        target = custom

    # Renormalize to sum to 1.0
    total = sum(target.values())
    if total > 0:
        for level in target:
            target[level] = target[level] / total

    return target

def calculate_resulting_fte(headcount: Dict[str, int], multipliers: Dict[str, float]) -> Dict[str, float]:
    """Calculate effective FTE from headcount and multipliers"""
    result = {}
    for level in ["L1", "L2", "L3", "L4", "L5"]:
        hc = headcount.get(level, 0)
        mult = multipliers.get(level, 1.0)
        result[level] = round(hc * mult, 2)
    return result

def recommend(
        fte_gap: float,
        priority: str,
        platforms: List[str],
        current_headcount: Dict[str, int],
        level_multipliers: Dict[str, float],
        db: Session,
        custom_target_share: Optional[Dict] = None,
        budget: Optional[Dict] = None
) -> Tuple[str, Dict, Dict, Dict, Dict]:
    """
    Generate role recommendation
    Returns: (mode, hire_plan, rebalance_plan, resulting_fte, explanation)
    """

    risk = classify_risk(fte_gap)
    constraints = load_constraints(priority, db)

    # NO-RISK short-circuit
    if risk == "NONE":
        resulting_fte = calculate_resulting_fte(current_headcount, level_multipliers)
        explanation = {
            "reason": f"Gap {fte_gap:.2f} < {NO_RISK_THRESHOLD} (no hire required)",
            "priority": priority,
            "risk": risk
        }
        return "NO_RISK", {}, {}, resulting_fte, explanation

    # Build target distribution
    target_share = build_target_share(priority, platforms, custom_target_share, db)

    # Calculate desired headcount additions per level
    want = {}
    for level in ["L5", "L4", "L3", "L2", "L1"]:
        share = target_share.get(level, 0.0)
        mult = level_multipliers.get(level, 1.0)
        if mult > 0:
            want[level] = (share * fte_gap) / mult
        else:
            want[level] = 0

    # Start with floor of desired counts
    hire_plan = {level: int(want[level]) for level in want}

    # Calculate covered FTE so far
    covered_fte = sum(
        hire_plan[level] * level_multipliers.get(level, 1.0)
        for level in hire_plan
    )

    remaining_gap = fte_gap - covered_fte

    # Greedy allocation of remaining gap
    while remaining_gap > 0.1:  # 0.1 FTE tolerance
        best_level = None
        best_score = float('inf')

        for level in ["L5", "L4", "L3", "L2", "L1"]:
            mult = level_multipliers.get(level, 1.0)
            if mult <= 0:
                continue

            overshoot = max(0, mult - remaining_gap)
            target_deviation = abs(want[level] - hire_plan.get(level, 0) - 1)

            score = overshoot * 2 + target_deviation

            if score < best_score:
                best_score = score
                best_level = level

        if best_level is None:
            break

        hire_plan[best_level] = hire_plan.get(best_level, 0) + 1
        remaining_gap -= level_multipliers.get(best_level, 1.0)

    # Clean up - remove zeros
    hire_plan = {k: v for k, v in hire_plan.items() if v > 0}

    # Calculate resulting headcount and FTE
    resulting_headcount = {
        level: current_headcount.get(level, 0) + hire_plan.get(level, 0)
        for level in ["L1", "L2", "L3", "L4", "L5"]
    }
    resulting_fte = calculate_resulting_fte(resulting_headcount, level_multipliers)

    # Build explanation
    explanation = {
        "reason": f"Need to hire {sum(hire_plan.values())} QA engineers to cover {fte_gap:.2f} FTE gap",
        "targetShare": target_share,
        "wantedHeadcount": {k: round(v, 2) for k, v in want.items()},
        "constraints": constraints,
        "priority": priority,
        "risk": risk,
        "remainingGap": round(max(0, remaining_gap), 2)
    }

    return "HIRE", hire_plan, {}, resulting_fte, explanation