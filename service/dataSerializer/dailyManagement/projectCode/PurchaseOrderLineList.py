from service.dataSerializer.IDataSerializer import IDataSerializer
import logging
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.database import db
from view.PoLineList import PoLineListSchema

logger = logging.getLogger(__name__)


class PurchaseOrderLineList(IDataSerializer):

    def __init__(self, ft, poNo, page, size):
        self.filter = ft
        self.page = page
        self.size = size
        self.poNo = poNo

    def serialize(self):
        self.filter.append(ObjPurchaseOrderDetail.po_no == self.poNo)
        result = db.session.query(ObjPurchaseOrderDetail) \
            .filter(*self.filter) \
            .order_by(ObjPurchaseOrderDetail.po_line_no) \
            .paginate(page=self.page, per_page=self.size, error_out=False)

        schema = PoLineListSchema()
        data = schema.dumps(result.items, many=True)
        if len(result.items) < self.size:
            return len(result.items), 1, data
        else:
            return result.total, result.pages, data
