from marshmallow import Schema, fields


class VendorChartSchema(Schema):
    site = fields.Str()
    vendor_code = fields.Str()
    vendor_name = fields.Str()
    amount = fields.Number()
