from pydantic import BaseModel, Field, create_model
from typing import List, Type, Any


class PaginationParams(BaseModel):
    page: int = Field(0, ge=0)
    page_size: int = Field(10, ge=10, le=100)


class PaginatedResponseSchema(BaseModel):
    page: int
    page_size: int
    count: int

    class Config:
        arbitrary_types_allowed = True


def create_paginated_response_schema(model: Type[BaseModel]) -> Type[PaginatedResponseSchema]:
    return create_model(
        model.__name__ + "PaginatedList",
        results=(List[model], ...),
        __base__=PaginatedResponseSchema
    )


def get_paginated_dict(results: List[Any], pagination: PaginationParams, count: int):
    return {"results": results, "page": pagination.page, "page_size": pagination.page_size, "count": count}
