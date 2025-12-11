from pydantic import BaseModel

class AgentStatus(BaseModel):
    name: str
    status: str
