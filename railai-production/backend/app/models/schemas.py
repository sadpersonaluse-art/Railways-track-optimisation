from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Train(BaseModel):
    train_id: int
    train_number: str
    train_name: str
    train_type: str
    scheduled_arrival: str
    scheduled_departure: str
    current_eta: str
    passenger_load: int
    priority: str
    assigned_platform: int
    status: str
    
    class Config:
        from_attributes = True

class Platform(BaseModel):
    platform_id: int
    capacity: int
    is_operational: bool
    proximity_to_concourse: str
    has_handicap_access: bool
    current_occupancy: int

class OptimizationRequest(BaseModel):
    trains: List[Train]
    platforms: List[Platform]

class OptimizationResponse(BaseModel):
    optimized_trains: List[Train]
    conflicts_resolved: int
    performance_metrics: Dict[str, Any]
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str = "1.0.0"