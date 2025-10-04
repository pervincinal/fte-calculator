# Find the Priority enum in app/models.py and replace it with:

from enum import Enum

class Priority(str, Enum):
    BUSINESS_CRITICAL = "BUSINESS_CRITICAL"
    MISSION_CRITICAL = "MISSION_CRITICAL"  
    BUSINESS_OPERATION = "BUSINESS_OPERATION"
    # Keep old values for backward compatibility
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
