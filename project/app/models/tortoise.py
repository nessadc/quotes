from tortoise import fields, models


class Quote(models.Model):
    quote = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    url = fields.TextField()

    def __str__(self):
        return self.quote
