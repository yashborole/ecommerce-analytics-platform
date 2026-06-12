from pydantic import BaseModel, Field, AnyUrl, field_validator,model_validator
from typing import Annotated, Literal, Operational, List
from uuid import UUID
from datetime import datetime

class product(BaseModel):
    id: UUID
    name: str
    
