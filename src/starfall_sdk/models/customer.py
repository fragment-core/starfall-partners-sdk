from uuid import UUID

from pydantic import BaseModel


class CustomerModel(BaseModel):
    uuid: UUID
    username: str


class CustomerSearchModel(BaseModel):
    uuid: UUID
    avatar: str
