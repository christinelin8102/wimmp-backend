from marshmallow import Schema, fields


class PurchaseAmountPerSiteSchema(Schema):
    bg = fields.Str()
    site = fields.Str()
    plant = fields.Str()
    amount = fields.Float()
