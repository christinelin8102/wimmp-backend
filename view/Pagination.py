from marshmallow import Schema, fields


class PaginationSchema(Schema):
    total = fields.Int()
    page = fields.Int()
