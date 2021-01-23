from marshmallow import Schema, fields


class PaymentTermSchema(Schema):
    code = fields.Str()
    payment_term = fields.Str()
    description = fields.Str()

