from pydantic import BaseModel
from typing import List, Dict, Optional

class MCPMessage(BaseModel):
    sender: str
    receiver: str
    type: str
    trace_id: str
    payload: Dict