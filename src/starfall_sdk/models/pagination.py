from pydantic import BaseModel


class PaginationModel[T](BaseModel):
    items: list[T]
    total: int
