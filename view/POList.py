from marshmallow import Schema, fields


class POListSchema(Schema):
    charge = fields.Float()
    po_no = fields.Str()
    charge_plant_code = fields.Str()
    amount = fields.Float()
    po_currency = fields.Str()
    vendor_code = fields.Str()
    vendor_name = fields.Str()
    pr_remark = fields.Str()
