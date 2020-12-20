from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import QuotePayloadSchema, QuoteResponseSchema
from app.models.tortoise import QuoteSchema
from typing import List

router = APIRouter()


@router.post("/", response_model=QuoteResponseSchema, status_code=201)
async def create_quote(payload: QuotePayloadSchema) -> QuoteResponseSchema:
    quote_id = await crud.post(payload)

    response_objet = {
        "id": quote_id,
        "value": payload.value
    }
    return response_objet


@router.get("/{id}/", response_model=QuoteSchema)
async def read_quote(id: int) -> QuoteSchema:
    quote = await crud.get(id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.get("/", response_model=List[QuoteSchema])
async def read_all_quotes() -> List[QuoteSchema]:
    return await crud.get_all()