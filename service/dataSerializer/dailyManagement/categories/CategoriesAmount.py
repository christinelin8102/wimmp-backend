from service.dataSerializer.IDataSerializer import IDataSerializer
import logging
import json
from model.PurchaseOrder import ObjPurchaseOrder
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.database import db
from sqlalchemy.sql import func
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from utils.ApiResponse import *

logger = logging.getLogger(__name__)


class CategoriesAmount(IDataSerializer):

    def __init__(self, ft, projectCode):
        self.filter = ft
        self.projectCode = projectCode

    def serialize(self):
        """
        SELECT "PURCHASE_ORDER_DETAIL".category,
        sum("PURCHASE_ORDER_DETAIL".po_line_amount) AS amount,
        count("PURCHASE_ORDER".po_no) AS po_count
        FROM "PURCHASE_ORDER_DETAIL"
        JOIN "PURCHASE_ORDER" ON "PURCHASE_ORDER".po_no = "PURCHASE_ORDER_DETAIL".po_no
        GROUP BY "PURCHASE_ORDER_DETAIL".category
        """
        try:
            result = db.session.query(ObjPurchaseOrderDetail.category,
                                      func.sum(ObjPurchaseOrderDetail.po_line_amount).label("amount"),
                                      func.count(ObjPurchaseOrder.po_no).label("count")) \
                .join(ObjPurchaseOrder, ObjPurchaseOrder.po_no == ObjPurchaseOrderDetail.po_no) \
                .filter(*self.filter) \
                .group_by(ObjPurchaseOrderDetail.category)

            total_amount = 0
            total_count = 0

            for res in result:
                total_amount = total_amount + res.amount
                total_count = total_count + res.count

            items = []
            for res in result:
                data = {'category': res.category,
                        'amount': float(res.amount),
                        'amount_percentage': float(res.amount / total_amount),
                        'count': res.count,
                        'count_percentage': float(res.count / total_count)}
                items.append(data)
        except ValidationError as err:
            items = ApiResponse.emitErrorOutput(E_VALIDATION_ERROR, err.messages, "DatabaseGetHeaderService")
        except SQLAlchemyError as e:
            db.session.rollback()
            items = ApiResponse.emitErrorOutput(E_SQLALCHEMY_ERROR, str(e), "DatabaseGetHeaderService")
        return json.dumps(items)
