from pydantic import BaseModel


class BaseSchema(BaseModel):
    model_config = {"from_attributes": True}


class HealthCheck(BaseSchema):
    status: str = "ok"
    timestamp: str
