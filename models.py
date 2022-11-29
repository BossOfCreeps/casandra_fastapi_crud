import os
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from cassandra.cluster import Cluster

from schemas import ExampleModelRequest

session = Cluster(os.getenv("CASANDRA_HOST", "127.0.0.1").split(" ")).connect('test')


class ExampleModel:
    __tablename__ = "example_model"

    example_id: UUID
    created_at: datetime
    description: str
    example_type: int

    def __init__(self, **kwargs):
        self.example_id = uuid4()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        session.execute(
            f"INSERT INTO {self.__tablename__} (\"example_id\", \"created_at\", \"description\", \"example_type\") "
            f"VALUES ({self.example_id}, '{self.created_at}', '{self.description}', {self.example_type});"
        )

    @classmethod
    def list(cls) -> List['ExampleModel']:
        result = []
        for row in session.execute(f"SELECT * FROM {cls.__tablename__};"):
            result.append(ExampleModel(**{field: getattr(row, field) for field in row._fields}))
        return result

    @classmethod
    def create(cls, data: ExampleModelRequest) -> 'ExampleModel':
        model = ExampleModel(**data.dict())
        model.save()
        return model

    @classmethod
    def read(cls, model_id: UUID) -> 'ExampleModel':
        item = session.execute(f"SELECT * FROM {cls.__tablename__} WHERE \"example_id\"={str(model_id)};").one()
        return ExampleModel(**{field: getattr(item, field) for field in item._fields})

    @classmethod
    def delete(cls, model_id: UUID):
        session.execute(f"DELETE FROM {cls.__tablename__} WHERE example_id = {model_id};")
