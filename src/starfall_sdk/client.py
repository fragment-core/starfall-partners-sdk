import asyncio
from http import HTTPMethod
from typing import Any, Self
from uuid import UUID

from aiohttp import ClientSession, ClientTimeout

from starfall_sdk.errors import StarFallSDKError
from starfall_sdk.models.agent import AgentModel, AgentRateModel
from starfall_sdk.models.customer import CustomerSearchModel
from starfall_sdk.models.pagination import PaginationModel
from starfall_sdk.models.transaction import TransactionModel


class StarFallSDK:
    BASE_URL = "https://api.partners.starfall.pw"

    def __init__(self, access_token: str) -> None:
        self.__access_token = access_token

        self.client: ClientSession | None = None

    async def _create_client(self) -> None:
        if self.client is None or self.client.closed:
            self.client = ClientSession(
                headers={"Authorization": f"Bearer {self.__access_token}"},
                timeout=ClientTimeout(15),
                base_url=self.BASE_URL,
            )

    async def _close_client(self) -> None:
        if self.client:
            if not self.client.closed:
                await self.client.close()
                await asyncio.sleep(0.15)

            self.client = None

    async def __aenter__(self) -> Self:
        await self._create_client()
        return self

    async def __aexit__(self, exc_type: object, exc: BaseException, tb: object) -> None:
        await self._close_client()

    async def _request[T](
        self,
        model: type[T],
        url: str,
        method: HTTPMethod = HTTPMethod.GET,
        body: dict[str, Any] | None = None,
        params: dict[str, str | int] | None = None,
    ) -> T:
        await self._create_client()

        # we are already created client in func before
        response = await self.client.request(  # type: ignore
            method=method,
            url=url,
            json=body,
            params=params,
        )

        data = await response.json()

        if data.get("error"):
            raise StarFallSDKError(
                message=data["message"],
                status_code=response.status,
            )

        return model(**data)

    async def get_me(self) -> AgentModel:
        return await self._request(
            AgentModel,
            url="/agent/me",
        )

    async def get_rate(self) -> AgentRateModel:
        return await self._request(
            AgentRateModel,
            url="/agent/rates",
        )

    async def get_transactions(
        self, offset: int, limit: int = 50
    ) -> PaginationModel[TransactionModel]:
        return await self._request(
            PaginationModel[TransactionModel],
            url="/agent/transactions",
            params={"limit": limit, "offset": offset},
        )

    async def search_recipient(self, query: str) -> CustomerSearchModel:
        return await self._request(
            CustomerSearchModel,
            url="/transactions/search",
            method=HTTPMethod.POST,
            body={"query": query},
        )

    async def create_transaction(
        self, customer_uuid: UUID | str, quantity: int, redirect_url: str
    ) -> TransactionModel:
        return await self._request(
            TransactionModel,
            url="/transactions/create",
            method=HTTPMethod.POST,
            body={
                "uuid": str(customer_uuid),
                "quantity": quantity,
                "redirect_url": redirect_url,
            },
        )

    async def get_transaction(self, transaction_id: UUID | str) -> TransactionModel:
        return await self._request(
            TransactionModel,
            url=f"/transactions/{transaction_id}",
        )
