from marshmallow import Schema, fields
from datetime import datetime


class ExceptionAlertReportSchema(Schema):
    id = fields.Int()
    alert_id = fields.Int()
    processed_by = fields.Str()
    plant_code = fields.Str()
    po_no = fields.Str()
    exception_id = fields.Int()
    rule_result = fields.Str()
    is_reasonable = fields.Bool()
    notes = fields.Str()
    files_link = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    created_by = fields.Int()
    updated_at = fields.DateTime("%Y-%m-%d %H:%M:%S", default=datetime.now())
    updated_by = fields.Int()
