from uuid import UUID

import uvicorn
from fastapi import FastAPI
from starlette import status

from models import ExampleModel
from schemas import ExampleModelResponse, ExampleModelPageScheme, ExampleModelRequest

app = FastAPI()


@app.get("/models/", response_model=ExampleModelPageScheme, status_code=status.HTTP_200_OK)
async def get_models():
    items = [ExampleModelResponse.from_orm(model) for model in ExampleModel.list()]
    return ExampleModelPageScheme(items=items, count=len(items))


@app.post("/models/", response_model=ExampleModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(item: ExampleModelRequest):
    model = ExampleModel.create(item)
    return ExampleModelResponse.from_orm(model)


@app.get("/models/{model_id}", response_model=ExampleModelResponse, status_code=status.HTTP_200_OK)
async def get_model(model_id: UUID):
    model = ExampleModel.read(model_id)
    return ExampleModelResponse.from_orm(model)


@app.put("/models/{model_id}", response_model=ExampleModelResponse, status_code=status.HTTP_200_OK)
async def put_model(model_id: UUID, item: ExampleModelRequest):
    model = ExampleModel.read(model_id)
    for key, value in item.dict().items():
        setattr(model, key, value)
    model.save()
    return ExampleModelResponse.from_orm(model)


@app.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: UUID):
    ExampleModel.delete(model_id)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
