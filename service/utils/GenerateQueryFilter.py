from model.PurchaseOrder import ObjPurchaseOrder
from model.Vendor import ObjVendor
from model.database import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GenerateQueryFilter:

    def __init__(self, fields):
        self.start_date = fields.startdate
        self.end_date = fields.enddate
        self.vendor_type = fields.vendor
        self.reimburse_type = fields.reimburseTag
        self.pageSize = fields.pageSize
        self.pageNo = fields.pageNo
        self.sort = fields.sort
        self.filter = fields.filter
        if fields.bg is not None:
            self.bg = fields.bg.split(",")
        if fields.site is not None:
            self.site = fields.site.split(",")
        if fields.plant is not None:
            self.plant = fields.plant.split(",")

    def generate_header_filter(self):
        start_date = datetime.fromtimestamp(self.start_date).strftime("%Y-%m-%d 00:00:00")
        end_date = datetime.fromtimestamp(self.end_date).strftime("%Y-%m-%d 23:59:59")

        ft = []
        if self.vendor_type == "Y":
            vendor = db.session.query(ObjVendor.vendor_code).all()
            ft.append(ObjPurchaseOrder.vendor_code.notin_(vendor))
        if self.reimburse_type == 1:
            ft.append(ObjPurchaseOrder.reimburse == True)
        elif self.reimburse_type == 2:
            ft.append(ObjPurchaseOrder.reimburse == False)
        else:
            reimburse_in_list = ''
        if self.bg is not None and len(self.bg) > 0:
            ft.append(ObjPurchaseOrder.mmp_bg.in_(self.bg))

        if self.site is not None and len(self.site) > 0:
            ft.append(ObjPurchaseOrder.mmp_site.in_(self.site))

        if self.plant is not None and len(self.plant) > 0:
            ft.append(ObjPurchaseOrder.charge_plant_code.in_(self.plant))

        ft.append(ObjPurchaseOrder.po_date.between(start_date, end_date))

        return ft
