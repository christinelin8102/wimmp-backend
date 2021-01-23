from service.dataSerializer.IDataSerializer import IDataSerializer
import logging
from model.PurchaseOrder import ObjPurchaseOrder
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.Charge import ObjCharge
from model.PurchaseRequest import ObjPurchaseRequest
from model.database import db
from sqlalchemy.sql import func
from view.POList import POListSchema

logger = logging.getLogger(__name__)


class PurchaseOrderList(IDataSerializer):

    def __init__(self, ft, projectCode, page, size):
        self.filter = ft
        self.page = page
        self.size = size
        self.projectCode = projectCode

    def serialize(self):
        self.filter.append(ObjCharge.charge_pcode == self.projectCode)
        result = db.session.query(ObjPurchaseOrder.po_no,
                                  ObjPurchaseOrder.charge_plant_code,
                                  func.sum(ObjPurchaseOrderDetail.po_line_amount).label("amount"),
                                  ObjPurchaseOrder.po_currency,
                                  ObjCharge.charge,
                                  ObjPurchaseOrder.vendor_code,
                                  ObjPurchaseOrder.vendor_name,
                                  ObjPurchaseRequest.pr_remark) \
            .join(ObjPurchaseOrderDetail, ObjPurchaseOrderDetail.po_no == ObjPurchaseOrder.po_no) \
            .join(ObjPurchaseRequest, ObjPurchaseRequest.pr_no == ObjPurchaseOrder.pr_no) \
            .join(ObjCharge, ObjCharge.pr_no == ObjPurchaseOrder.pr_no) \
            .filter(*self.filter) \
            .group_by(ObjPurchaseOrder.po_no, ObjCharge.charge, ObjPurchaseRequest.pr_remark) \
            .paginate(self.page, self.size)

        schema = POListSchema()
        data = schema.dumps(result.items, many=True)
        return result.total, result.pages, data
