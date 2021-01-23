import logging
import json
import datetime
from service.dataSerializer.IDataSerializer import IDataSerializer
from service.dataSerializer.GetDataService import GetDataService
from utils.ApiResponse import *
from itertools import groupby
from operator import itemgetter
import datetime

from model.Plant import ObjPlant
from model.Site import ObjSite
from model.BG import ObjBG
from model.PurchaseOrder import ObjPurchaseOrder
from model.database import db
from view.Header import HeaderSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class DatabaseGetPOTop10Service(IDataSerializer):

    def __init__(self, req):
        self.req = req
        pass

    def serialize(self):
        bg = self.req.bg
        site = self.req.site
        plant = self.req.plant
        startdate = self.req.startdate
        enddate = self.req.enddate
        datetime_start = datetime.datetime.fromtimestamp(startdate)
        datetime_end = datetime.datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')
        print(dtStartStr)
        print(dtEndStr)

        logger.debug("------DatabaseGetPOTop10Service Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))

        queryTyoe = 0
        if bg == '' and site == '' and plant == '':
            queryTyoe = 1
        if queryTyoe == 1:
            sqlquery = 'select \'PO00\'||id as id, pono, amount, pcode, vendername, remark ' \
                       'from (select row_number() OVER(ORDER BY po.po_no) as id, ' \
                       'po.po_no as pono ,po.po_amount as amount, poc.mmp_charge_code as pcode, ' \
                       'po.vendor_name as vendername , pr.pr_remark as remark ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'LEFT OUTER JOIN public."PURCHASE_REQUEST" pr ' \
                       'on po.pr_no = pr.pr_no ' \
                       'inner join public."PURCHASE_ORDER_CHARGE" poc '\
                       'on po.po_no = poc.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' ' \
                       ') as temp limit 10'
        else:
            sqlquery = 'select \'PO00\'||id as id, pono, amount, pcode, vendername, remark ' \
                       'from (select row_number() OVER(ORDER BY po.po_no) as id, ' \
                       'po.po_no as pono ,po.po_amount as amount, poc.mmp_charge_code as pcode, ' \
                       'po.vendor_name as vendername , pr.pr_remark as remark ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'LEFT OUTER JOIN public."PURCHASE_REQUEST" pr ' \
                       'on po.pr_no = pr.pr_no ' \
                       'inner join public."PURCHASE_ORDER_CHARGE" poc ' \
                       'on po.po_no = poc.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' '
            if plant != '':
                sqlquery += 'and charge_plant_code in (' + str(plant.split(',')).replace('[', '').replace(']', '') + ')'
            if bg != '':
                sqlquery += 'and mmp_bg in (' + str(bg.split(',')).replace('[', '').replace(']', '') + ')'
            if site != '':
                sqlquery += 'and mmp_site in (' + str(site.split(',')).replace('[', '').replace(']', '') + ')'

            sqlquery += 'group by po.po_no, poc.mmp_charge_code, pr.pr_remark, charge_plant_code, mmp_site, mmp_bg, to_char(po_date, \'YYYY/MM\') order by po.po_no, poc.mmp_charge_code, pr.pr_remark, charge_plant_code, mmp_site, mmp_bg, to_char(po_date, \'YYYY/MM\')) as temp limit 10'
        print(sqlquery)
        data = GetDataService.getdata(self, sqlquery)
        print(data)
        if data == []:
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        ostr = ''
        for index, value in enumerate(data):
            i = index + 1
            if i < len(data):
                ostr += '"' + str(i) + '" : ' + '{ "poNo" : "' + value[0] + '", "item" : "' \
                         + value[1] + '", "poAmount" : "' \
                         + str(value[2]) + '", "poOrDeptCode" : "' \
                         + value[3] + '", "vendorName" : "' \
                         + value[4] + '", "prRemark" : "' \
                         + str(value[5]) + '" },'
            elif i == len(data):
                ostr += '"' + str(i) + '" : ' + '{ "poNo" : "' + value[0] + '", "item" : "' \
                         + value[1] + '", "poAmount" : "' \
                         + str(value[2]) + '", "poOrDeptCode" : "' \
                         + value[3] + '", "vendorName" : "' \
                         + value[4] + '", "prRemark" : "' \
                         + str(value[5]) + '" }'
        strjson = '{' + ostr + '}'
        print(strjson.replace("\r\n", ""))
        strjson = strjson.replace("\r\n", "")
        json_data = strjson
        if json_data is not None:
            dataJsonArray = json.loads(json_data)
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        return result