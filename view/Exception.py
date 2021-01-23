from marshmallow import Schema, fields
from datetime import datetime


class ExceptionSchema(Schema):
    id = fields.Int()
    alert_id = fields.Int()
    # triggered_date = fields.DateTime()
    # assigned_to = fields.Str()
    # processed_by = fields.Str()
    # plant_code = fields.Str()
    po_no = fields.Str()
    po_line_no = fields.Str()
    po_currency = fields.Str()
    po_price = fields.Number()
    po_line_amount = fields.Number()
    # exception_id = fields.Int()
    rule_result = fields.Str()
    # is_reasonable = fields.Bool()
    notes = fields.Str()
    files_link = fields.Str()
    # status = fields.Str()
    vendor_code = fields.Str()
    vendor_name = fields.Str()
    pr_remark = fields.Str()
    created_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    created_by = fields.Int()
    updated_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    updated_by = fields.Int()
