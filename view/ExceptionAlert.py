from marshmallow import Schema, fields
from datetime import datetime


class ExceptionAlertSchema(Schema):
    id = fields.Int()
    alert_id = fields.Int()
    triggered_date = fields.DateTime()
    plant_code = fields.Str()
    po_no = fields.Str()
    exception_id = fields.Int()
    rule_result = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    created_by = fields.Int()
    updated_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    updated_by = fields.Int()
