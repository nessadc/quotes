from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.tortoise import QuoteSchema

from app.models.pydantic import (  # isort:skip
    QuotePayloadSchema,
    QuoteResponseSchema,
    QuoteUpdatePayloadSchema,
)

router = APIRouter()


@router.post("/", response_model=QuoteResponseSchema, status_code=201)
async def create_quote(payload: QuotePayloadSchema) -> QuoteResponseSchema:
    quote_id = await crud.post(payload)

    response_objet = {"id": quote_id, "value": payload.value}
    return response_objet


@router.get("/{id}/", response_model=QuoteSchema)
async def read_quote(id: int = Path(..., gt=0)) -> QuoteSchema:
    quote = await crud.get(id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote


@router.get("/", response_model=List[QuoteSchema])
async def read_all_quotes() -> List[QuoteSchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=QuoteResponseSchema)
async def delete_quote(id: int = Path(..., gt=0)) -> QuoteResponseSchema:
    quote = await crud.get(id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    await crud.delete(id)

    return quote


@router.put("/{id}/", response_model=QuoteSchema)
async def update_quote(id: int, payload: QuoteUpdatePayloadSchema) -> QuoteSchema:
    quote = await crud.put(id, payload)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    return quote
