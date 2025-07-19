# StarFall API SDK

Python SDK для интеграции с StarFall Partners API  
[![Telegram Support](https://img.shields.io/badge/Telegram-StarFall%20Sales-blue?logo=telegram)](https://t.me/starfall_sales) <br>
Документация API https://api.partners.starfall.pw/docs

## Установка

```bash
pip install starfall-sdk
# или
poetry add starfall-sdk
```

## Flow работы с API

- Поиск пользователя
- Создание транзакции
- Обработка уведомлений (опционально)

## Пример

```python
from starfall_sdk import StarFallSDK, StarFallSDKError

async def main():
    async with StarFallSDK(access_token="...") as client:
        try:
            # Поиск пользователя
            customer = await client.search_recipient("@username")

            # Создание транзакции
            transaction = await client.create_transaction(
                customer_uuid=customer.uuid,
                quantity=100,
                redirect_url="https://your-service.com",
            )

            print(f"Payment URL: {transaction.payment_url}")
        except StarFallSDKError as e:
            print(f"Error [{e.status_code}]: {e.detail}")
```

### Структура уведомления

```json
{
    "id": int,
    "agent_id": int,
    "customer": {
        "uuid": "uuid4",
        "username": "str"
    },
    "amount": float,
    "quantity": int,
    "reward": float,
    "status": "created|paid|success|failed"
}
```

## Обработка уведомлений

```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starfall_sdk import TransactionStatus


class CustomerSchema(BaseModel):
    uuid: UUID
    username: str


class WebhookSchema(BaseModel):
    id: int
    agent_id: int

    customer: CustomerSchema

    amount: float
    quantity: int
    reward: float

    status: TransactionStatus


app = FastAPI()

@app.post("/webhook/starfall")
async def handle_webhook(event: WebhookSchema):
    if event.status == TransactionStatus.SUCCESS:
        print(f"Транзакция #{event.id} успешно завершена!")
        print(f"Пользователь: {event.customer.username}")
        print(f"Начислено: {event.quantity} единиц")
    elif event.status == TransactionStatus.PAID:
        print(f"Пользоватиль оплатил заказ #{event.id}!")
    elif event.status == TransactionStatus.FAILED:
        print(f"Транзакция #{event.id} не удалась")

    return {"status": "ok"}
```
