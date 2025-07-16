import enum


class TransactionStatus(enum.StrEnum):
    CREATED = "created"
    PAID = "paid"
    SUCCESS = "success"
    FAILED = "failed"
