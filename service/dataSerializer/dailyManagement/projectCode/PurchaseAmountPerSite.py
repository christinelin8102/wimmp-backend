from service.dataSerializer.IDataSerializer import IDataSerializer
import logging
from model.PurchaseOrder import ObjPurchaseOrder
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.Charge import ObjCharge
from model.database import db
from sqlalchemy.sql import func
from view.PurchaseAmountPerSite import PurchaseAmountPerSiteSchema

logger = logging.getLogger(__name__)


class PurchaseAmountPerSite(IDataSerializer):

    def __init__(self, ft, projectCode, page, size):
        self.filter = ft
        self.page = page
        self.size = size
        self.projectCode = projectCode

    def serialize(self):
        """
        SELECT "PURCHASE_ORDER".mmp_site AS site,
        "PURCHASE_ORDER".mmp_bg AS bg,
        "PURCHASE_ORDER".charge_plant_code AS plant,
        sum("PURCHASE_ORDER_DETAIL".po_line_amount) AS amount
        FROM "PURCHASE_ORDER"
        JOIN "PURCHASE_ORDER_DETAIL" ON "PURCHASE_ORDER_DETAIL".po_no = "PURCHASE_ORDER".po_no
        JOIN "CHARGE" ON "CHARGE".pr_no = "PURCHASE_ORDER".pr_no
        GROUP BY "PURCHASE_ORDER".mmp_site, "PURCHASE_ORDER".mmp_bg, "PURCHASE_ORDER".charge_plant_code
        """
        self.filter.append(ObjCharge.charge_pcode == self.projectCode)
        result = db.session.query(ObjPurchaseOrder.mmp_site.label('site'),
                                  ObjPurchaseOrder.mmp_bg.label('bg'),
                                  ObjPurchaseOrder.charge_plant_code.label('plant'),
                                  func.sum(ObjPurchaseOrderDetail.po_line_amount).label("amount")) \
            .join(ObjPurchaseOrderDetail, ObjPurchaseOrderDetail.po_no == ObjPurchaseOrder.po_no) \
            .join(ObjCharge, ObjCharge.pr_no == ObjPurchaseOrder.pr_no) \
            .filter(*self.filter) \
            .group_by(ObjPurchaseOrder.mmp_site, ObjPurchaseOrder.mmp_bg, ObjPurchaseOrder.charge_plant_code) \
            .paginate(self.page, self.size)

        schema = PurchaseAmountPerSiteSchema()
        data = schema.dumps(result.items, many=True)
        return result.total, result.pages, data
