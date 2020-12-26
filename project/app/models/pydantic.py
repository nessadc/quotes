from pydantic import BaseModel


class QuotePayloadSchema(BaseModel):
    value: str


class QuoteResponseSchema(QuotePayloadSchema):
    id: int


class QuoteUpdatePayloadSchema(QuotePayloadSchema):
    value: str
