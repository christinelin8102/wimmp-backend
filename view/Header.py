from marshmallow import Schema, fields


class HeaderSchema(Schema):
    plant = fields.Str()
    site = fields.Str()
    bg = fields.Str()

