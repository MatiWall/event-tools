import time
import uuid

from pydantic import BaseModel, Field

class Metadata(BaseModel):
    timestamp: float = Field(default_factory=time.time)
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class Event(BaseModel):
    type: str
    body: object
    metadata: Metadata = Field(default_factory=Metadata)