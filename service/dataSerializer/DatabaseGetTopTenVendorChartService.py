from service.dataSerializer.IDataSerializer import IDataSerializer
from utils.ApiResponse import *
from model.Plant import ObjPlant
from model.Site import ObjSite
from model.BG import ObjBG
from model.database import db
from model.Vendor import ObjVendor
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.PurchaseOrder import ObjPurchaseOrder
from view.VendorChart import VendorChartSchema
import datetime
import logging

logger = logging.getLogger(__name__)
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

plant = ObjPlant()
bg = ObjBG()
site = ObjSite()
vendor = ObjVendor()
objPurchaseOrderDetail = ObjPurchaseOrderDetail()
vendorChartSchema = VendorChartSchema()


class DatabaseGetTopTenVendorChartService(IDataSerializer):
    def __init__(self, bg, site, plant, startdate, enddate, vendor_type, reimburse_type):
        self.bg = bg
        self.site = site
        self.plant = plant
        self.startdate = startdate
        self.enddate = enddate
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type
        pass

    def serialize(self):
        bg = self.bg
        site = self.site
        plant = self.plant
        startdate = self.startdate
        enddate = self.enddate
        vendor_type = self.vendor_type
        reimburse_type = self.reimburse_type
        datetime_start = datetime.datetime.fromtimestamp(startdate)
        datetime_end = datetime.datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')
        print(dtStartStr)
        print(dtEndStr)

        logger.debug("------DatabaseGetMonthlyPurchaseAmountService Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))
        """取得 plant site BG"""
        """ return
            {
                {
                    "site": "string",
                    "vendorList": [
                        {
                            "vendorCode": "string", # 第一名Vendor
                            "vendorName": "string",
                            "amount": 123
                        },
                        {
                            "vendorCode": "string", # 第二名Vendor
                            "vendorName": "string",
                            "amount": 123
                        }
                    ]
                },
        """
        # todo dao count amount po_number (po_price_in_ntd 尚為空)
        '''select po.vendor_code  as vandercode, po.vendor_name  as vendername
        ,sum(pod.po_price) as amount 
        ,po.mmp_site
        from public."PURCHASE_ORDER" po
		inner join public."PURCHASE_ORDER_DETAIL" pod ON po.po_no = pod.po_no
        where po.vendor_code in 
        (select vendor_code from public."PURCHASE_ORDER"
        group by vendor_code order by sum(po_amount) desc limit 10)
		and po.mmp_site = 'APB'
        group by po.vendor_code ,po.vendor_name 
 		,po.mmp_site
        order by po.vendor_code'''
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
            # todo vendor_code >> mmp_vendor_code vendor_name >> mmp_vendor_name po_amount >> po_amount_in_ntd po_price >> po_price_in_ntd
            subq = db.session.query(ObjPurchaseOrder.vendor_code.label('vendor_code')).group_by(
                ObjPurchaseOrder.vendor_code).order_by(func.sum(ObjPurchaseOrder.po_amount).desc()).limit(10).subquery()

            ft.append(ObjPurchaseOrder.vendor_code.in_(subq))

            results = db.session.query(ObjPurchaseOrder.vendor_code.label('vendor_code'),
                                      ObjPurchaseOrder.vendor_name.label('vendor_name'),
                                      func.sum(ObjPurchaseOrderDetail.po_price).label('amount'),
                                      ObjPurchaseOrder.mmp_site.label('site')) \
                .join(ObjPurchaseOrderDetail, ObjPurchaseOrder.po_no == ObjPurchaseOrderDetail.po_no) \
                .filter(*ft).group_by(ObjPurchaseOrder.vendor_code, ObjPurchaseOrder.vendor_name,
                                      ObjPurchaseOrder.mmp_site).order_by(ObjPurchaseOrder.vendor_code)


            data = vendorChartSchema.dumps(results, many=True)

            logger.debug(data)
            return data
        except ValidationError as err:
            result = ApiResponse.emitErrorOutput(E_VALIDATION_ERROR, err.messages, "DatabaseGetHeaderService")
        except SQLAlchemyError as e:
            db.session.rollback()
            result = ApiResponse.emitErrorOutput(E_SQLALCHEMY_ERROR, str(e), "DatabaseGetHeaderService")
        return result
