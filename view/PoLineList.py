from marshmallow import Schema, fields


class PoLineListSchema(Schema):
    po_line_no = fields.Str()
    description = fields.Str()
    specification = fields.Str()
    po_qty = fields.Float()
    unit = fields.Str()
    po_price = fields.Str()
    po_line_amount = fields.Str()
    im_pn = fields.Str()
