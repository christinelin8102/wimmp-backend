'''
daily mngm top 10 P code: sql for DB
List - Button
'''

import json
from datetime import datetime
import pandas as pd
import numpy as np
from service.dataSerializer.IDataSerializer import IDataSerializer
from service.dataSerializer.GetDataService import GetDataService
import logging
from model.PurchaseOrder import ObjPurchaseOrder
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.PurchaseOrderCharge import ObjPurchaseOrderCharge
from model.PurchaseRequest import ObjPurchaseRequest
from model.PurchaseRequestDetail import ObjPurchaseRequestDetail
from model.Charge import ObjCharge
from model.Vendor import ObjVendor
from model.database import db
from io import StringIO
from flask import make_response

logger = logging.getLogger(__name__)


class DBPcodeListButton(IDataSerializer):

    def __init__(self, pcode, bg_list, site_list, plant_list, start_score, end_score, vendor_type, reimburse_type):
        self.bg = bg_list
        self.site = site_list
        self.plant = plant_list
        self.s_score = start_score
        self.e_score = end_score
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type
        self.p_code = pcode

        logger.debug('''------DailyMngmPcode : {7} \
            \n
            With Param: \
            \n
            BG: {0},
            \n
            SITE: {1},
            \n
            PLANT: {2},
            \n
            score between: {3} and {4}, 
            \n
            isIgnoreVendor: {5}, Reimburse: {6}'''.format(self.bg, self.site, self.plant,
                                                          self.s_score, self.e_score,
                                                          self.vendor_type, self.reimburse_type, self.p_code))

    def serialize(self):
        # transfer date for SQL
        s_date = datetime.fromtimestamp(self.s_score).strftime("%Y-%m-%d 00:00:00")  # %H:%M:%S
        e_date = datetime.fromtimestamp(self.e_score).strftime("%Y-%m-%d 23:59:59")

        filter = [ObjCharge.charge_pcode == self.p_code]

        if self.vendor_type == "Y":
            vendor = db.session.query(ObjVendor.vendor_code).all()
            filter.append(ObjPurchaseOrder.vendor_code.notin_(vendor))
        if self.reimburse_type == 1:
            filter.append(ObjPurchaseOrder.reimburse == True)
        elif self.reimburse_type == 2:
            filter.append(ObjPurchaseOrder.reimburse == False)
        else:
            reimburse_in_list = ''

        if self.bg is not None and len(self.bg) > 0:
            filter.append(ObjPurchaseOrder.mmp_bg.in_(self.bg))

        if self.site is not None and len(self.site) > 0:
            filter.append(ObjPurchaseOrder.mmp_site.in_(self.site))

        if self.plant is not None and len(self.plant) > 0:
            filter.append(ObjPurchaseOrder.charge_plant_code.in_(self.plant))

        filter.append(ObjPurchaseOrder.po_date.between(s_date, e_date))

        result = db.session.query(ObjPurchaseRequest.pr_no,
                                  ObjPurchaseRequest.pr_approve_date,
                                  ObjPurchaseRequest.applicant,
                                  ObjPurchaseRequest.applicant_dept,
                                  ObjPurchaseRequest.pr_type,
                                  ObjPurchaseRequest.sub_type,
                                  ObjPurchaseRequest.pr_currency,
                                  ObjPurchaseRequest.pr_exch_rate,
                                  ObjPurchaseRequest.pr_remark,
                                  ObjPurchaseRequestDetail.pr_line_no,
                                  ObjPurchaseRequestDetail.pr_qty,
                                  ObjPurchaseRequestDetail.pr_price,
                                  ObjPurchaseRequestDetail.part_no,
                                  ObjCharge.charge_deptcode,
                                  ObjCharge.charge_pcode,
                                  ObjCharge.charge,
                                  ObjPurchaseOrder.po_no,
                                  ObjPurchaseOrder.buyer_name,
                                  ObjPurchaseOrder.cancel_reject_remark,
                                  ObjPurchaseOrder.po_date,
                                  ObjPurchaseOrder.po_approve_date,
                                  ObjPurchaseOrder.vendor_code,
                                  ObjPurchaseOrder.vendor_name,
                                  ObjPurchaseOrder.vendor2_code,
                                  ObjPurchaseOrder.vendor2_name,
                                  ObjPurchaseOrder.tax_rate,
                                  ObjPurchaseOrder.delivery_term,
                                  ObjPurchaseOrder.delivery_date,
                                  ObjPurchaseOrder.payment_term,
                                  ObjPurchaseOrder.mmp_payment_code,
                                  ObjPurchaseOrder.po_currency,
                                  ObjPurchaseOrder.po_exch_rate,
                                  ObjPurchaseOrder.po_type1,
                                  ObjPurchaseOrder.po_type2,
                                  ObjPurchaseOrder.po_flag,
                                  ObjPurchaseOrder.reimburse,
                                  ObjPurchaseOrder.company,
                                  ObjPurchaseOrder.site,
                                  ObjPurchaseOrder.approve_flag,
                                  ObjPurchaseOrder.warranty,
                                  ObjPurchaseOrder.charge_plant_code,
                                  ObjPurchaseOrder.mmp_bg,
                                  ObjPurchaseOrder.mmp_site,
                                  ObjPurchaseOrderDetail.po_line_no,
                                  ObjPurchaseOrderDetail.description,
                                  ObjPurchaseOrderDetail.specification,
                                  ObjPurchaseOrderDetail.po_qty,
                                  ObjPurchaseOrderDetail.unit,
                                  ObjPurchaseOrderDetail.po_price,
                                  ObjPurchaseOrderDetail.price_before_tax,
                                  ObjPurchaseOrderDetail.im_pn,
                                  ObjPurchaseOrderDetail.category,
                                  ObjPurchaseOrderDetail.im_confidential,
                                  ObjPurchaseOrderDetail.only_check_amount) \
            .outerjoin(ObjPurchaseOrderDetail, ObjPurchaseOrder.po_no == ObjPurchaseOrderDetail.po_no) \
            .outerjoin(ObjPurchaseRequest, ObjPurchaseOrder.pr_no == ObjPurchaseRequest.pr_no) \
            .outerjoin(ObjPurchaseRequestDetail, ObjPurchaseRequest.pr_no == ObjPurchaseRequestDetail.pr_no) \
            .outerjoin(ObjCharge, ObjPurchaseRequestDetail.pr_no == ObjCharge.pr_no).all()

        try:
            df = pd.DataFrame(list(result))
            csv_file = StringIO()
            df.to_csv(csv_file, encoding='utf-8')
            csv_output = csv_file.getvalue()
            csv_file.close()
            response = make_response(csv_output)
            response.headers["Content-Disposition"] = "attachment; filename=latestVendorList.csv"
            response.headers["Content-Type"] = "text/csv"
            return response
        except Exception as ex:
            logger.debug("Fail! Reason: {}".format(ex))
            return None
