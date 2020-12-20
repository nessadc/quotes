from typing import List, Union

from app.models.pydantic import QuotePayloadSchema
from app.models.tortoise import Quote


async def post(payload: QuotePayloadSchema) -> int:
    quote = Quote(value=payload.value)
    await quote.save()
    return quote.id


async def get(id: int) -> Union[dict, None]:
    quote = await Quote.filter(id=id).first().values()
    if quote:
        return quote[0]
    return None


async def get_all() -> List:
    quotes = await Quote.all().values()
    return quotes
