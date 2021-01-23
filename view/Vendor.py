from marshmallow import Schema, fields


class VendorSchema(Schema):
    vendor_code = fields.Str()
    brief_name = fields.Str()
    full_name = fields.Str()
    chinese_full_name = fields.Str()
    location = fields.Str()


