from marshmallow import Schema, fields
from datetime import datetime


class VendorListSchema(Schema):
    vendor_code = fields.Str()
    vendor_name = fields.Str()
    amount = fields.Number()
    po_number = fields.Int()
    created_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    created_by = fields.Int()
    updated_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    updated_by = fields.Int()
