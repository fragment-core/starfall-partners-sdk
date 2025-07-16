from pydantic import BaseModel

from starfall_sdk.enums.transaction import TransactionStatus
from starfall_sdk.models.customer import CustomerModel


class TransactionModel(BaseModel):
    id: int
    agent_id: int

    customer: CustomerModel

    amount: float
    quantity: int
    reward: float

    payment_url: str
    status: TransactionStatus
