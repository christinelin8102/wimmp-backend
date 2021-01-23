from service.dataSerializer.IDataSerializer import IDataSerializer
from utils.ApiResponse import *
from model.Plant import ObjPlant
from model.Site import ObjSite
from model.BG import ObjBG
from model.database import db
from model.Vendor import ObjVendor
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.PurchaseOrder import ObjPurchaseOrder
from view.VendorList import VendorListSchema
import datetime
import logging
import math

logger = logging.getLogger(__name__)
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

plant = ObjPlant()
bg = ObjBG()
site = ObjSite()
vendor = ObjVendor()
objPurchaseOrderDetail = ObjPurchaseOrderDetail()
vendorListSchema = VendorListSchema()


class DatabaseGetTopTenVendorListService(IDataSerializer):
    def __init__(self, bg, site, plant, startdate, enddate, vendor_type, reimburse_type, pageSize, pageNo):
        self.bg = bg
        self.site = site
        self.plant = plant
        self.startdate = startdate
        self.enddate = enddate
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type
        self.pageSize = pageSize
        self.pageNo = pageNo
        pass

    def serialize(self):
        bg = self.bg
        site = self.site
        plant = self.plant
        startdate = self.startdate
        enddate = self.enddate
        vendor_type = self.vendor_type
        reimburse_type = self.reimburse_type
        pageSize = self.pageSize
        pageNo = self.pageNo
        datetime_start = datetime.datetime.fromtimestamp(startdate)
        datetime_end = datetime.datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')
        print(dtStartStr)
        print(dtEndStr)
        dictData = {}

        logger.debug("------DatabaseGetMonthlyPurchaseAmountService Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))
        """取得 plant site BG"""
        """ return 
            [{
              "vendor_code":"vCode1",
              "vendor_name":"vendor1",
              "amount":1234567,
              "po_number":1234
            }]
        """
        # todo vendor_code >> mmp_vendor_code vendor_name >> mmp_vendor_name po_amount >> po_amount_in_ntd po_price >> po_price_in_ntd
        try:
            ft = []
            if bg[0] != '':
                ft.append(ObjPurchaseOrder.mmp_bg.in_(bg))
            if site[0] != '':
                ft.append(ObjPurchaseOrder.mmp_site.in_(site))
            if plant[0] != '':
                ft.append(ObjPurchaseOrder.charge_plant_code.in_(plant))
            ft.append(ObjPurchaseOrder.po_date >= dtStartStr)
            ft.append(ObjPurchaseOrder.po_date <= dtEndStr)
            subq = db.session.query(func.count(ObjPurchaseOrderDetail.po_no).label('po_number'),
                                    # func.sum(ObjPurchaseOrderDetail.po_price_in_ntd).label('amount'),
                                    func.sum(ObjPurchaseOrderDetail.po_price).label('amount'),
                                    ObjPurchaseOrder.mmp_vendor_code.label('mmp_vendor_code')) \
                .join(ObjPurchaseOrder, ObjPurchaseOrder.po_no == ObjPurchaseOrderDetail.po_no) \
                .filter(*ft) \
                .group_by(ObjPurchaseOrder.mmp_vendor_code).subquery()

            results = db.session.query(ObjVendor.vendor_code.label('vendor_code'),
                                       ObjVendor.brief_name.label('vendor_name'),
                                       subq.c.po_number,
                                       subq.c.amount
                                       ) \
                .join(subq, subq.c.mmp_vendor_code == ObjVendor.vendor_code) \
                .join(ObjPurchaseOrder, ObjVendor.vendor_code == ObjPurchaseOrder.mmp_vendor_code) \
                .join(ObjPurchaseOrderDetail, ObjPurchaseOrder.po_no == ObjPurchaseOrderDetail.po_no)

            totalrows = results.count()
            data = vendorListSchema.dumps(results, many=True)
            logger.debug(data)
            # todo get totalpage

            dictData["totalPage"] = math.ceil(totalrows / pageSize)
            dictData["totalCount"] = totalrows
            dictData["data"] = data
            return dictData
            # return ApiResponse.emitSuccessOutput({"result": data})
        except ValidationError as err:
            result = ApiResponse.emitErrorOutput(E_VALIDATION_ERROR, err.messages, "DatabaseGetHeaderService")
        except SQLAlchemyError as e:
            db.session.rollback()
            result = ApiResponse.emitErrorOutput(E_SQLALCHEMY_ERROR, str(e), "DatabaseGetHeaderService")
        return result
