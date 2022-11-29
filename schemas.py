from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel


class ExampleModelRequest(BaseModel):
    created_at: datetime
    description: str
    example_type: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "created_at": datetime.now(),
                "description": "string",
                "example_type": 10,
            }
        }


class ExampleModelResponse(ExampleModelRequest):
    example_id: UUID

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "example_id": uuid4(),
                **ExampleModelRequest.Config.schema_extra["example"],
            }
        }


class ExampleModelPageScheme(BaseModel):
    items: List[ExampleModelResponse]
    count: int

    class Config:
        schema_extra = {
            "example": {
                "count": "1",
                "items": [ExampleModelResponse.Config.schema_extra["example"]],
            }
        }
