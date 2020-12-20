from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Quote(models.Model):
    value = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.value


QuoteSchema = pydantic_model_creator(Quote)
