from pydantic import BaseModel


class AgentModel(BaseModel):
    name: str
    balance: float
    commission: int


class AgentRateModel(BaseModel):
    star: float
