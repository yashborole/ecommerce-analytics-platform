from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str

class PlantBase(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[str] = None

class PlantCreate(PlantBase):
    pass

class PlantResponse(PlantBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    plants: list[PlantResponse] = []

    model_config = {"from_attributes": True}


# --- Machine Schemas ---

class MachineResponse(BaseModel):
    id: int
    name: str
    machine_type: Optional[str] = None
    status: str
    plant_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Dashboard Schemas ---

class DashboardKPI(BaseModel):
    total_production: int
    active_machines: int
    total_machines: int
    efficiency: float
    active_alerts: int
    downtime_machines: int

class ActivityLogResponse(BaseModel):
    id: int
    event: str
    status: str
    timestamp: datetime

    model_config = {"from_attributes": True}

class AlertResponse(BaseModel):
    id: int
    message: str
    severity: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class MachineInsight(BaseModel):
    id: int
    name: str
    machine_type: Optional[str] = None
    status: str
    total_produced: int
    target_units: int
    efficiency: float

    model_config = {"from_attributes": True}