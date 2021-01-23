import logging
import json
import datetime
from service.dataSerializer.IDataSerializer import IDataSerializer
from service.dataSerializer.GetDataService import GetDataService
from utils.ApiResponse import *
from itertools import groupby
from operator import itemgetter


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


class DatabaseVenderTop10Service(IDataSerializer):

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

        logger.debug("------DatabaseVenderTop10Service Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))
        size = ''
        queryTyoe = 0
        if bg == '' and site == '' and plant == '':
            queryTyoe = 1
        if queryTyoe == 1:
            sqlquery = 'select po.mmp_site as site, po.vendor_code  as vandercode, po.vendor_name  as vendername, sum(po.po_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'where po.vendor_code in (select vendor_code from public."PURCHASE_ORDER" ' \
                       'group by vendor_code, mmp_site order by sum(po_amount) desc limit 10) ' \
                       'and po.mmp_site is not null ' \
                       'group by po.vendor_code ,po.vendor_name, po.mmp_site ' \
                       'order by po.mmp_site'
        else:
            size = len(site.split(','))
            sqlquery = 'select po.mmp_site as site, po.vendor_code  as vandercode, po.vendor_name  as vendername, sum(po.po_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'where po.vendor_code in (select vendor_code from public."PURCHASE_ORDER" ' \
                       'group by vendor_code, mmp_site order by sum(po_amount) desc limit 10) ' \
                       'and po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' '
            if plant != '':
                sqlquery += 'and charge_plant_code in (' + str(plant.split(',')).replace('[','').replace(']','') + ')'
            if site != '':
                sqlquery += 'and mmp_site in (' + str(site.split(',')).replace('[','').replace(']','') + ')'

            sqlquery += 'group by po.vendor_code ,po.vendor_name, po.mmp_site order by po.mmp_site'

        print(sqlquery)
        data = GetDataService.getdata(self, sqlquery)
        print(data)
        if data == []:
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        result = []
        json_result = []
        format_string = ''
        column = ('site', 'vendorCode', 'vendorName', 'amount')
        for row in data:
            result.append(dict(zip(column, row)))
        old_site = ''
        for amountdata in result:
            if old_site != amountdata.get('site') and old_site != '':
                format_string += '"' + old_site + '":' + str(json_result) + ','
                old_site = amountdata.get('site')
                ammount = str(amountdata.get('amount'))
                del amountdata['site']
                amountdata['amount'] = ammount
                json_result = []
                json_result.append(amountdata)
            else:
                old_site = amountdata.get('site')
                ammount = str(amountdata.get('amount'))
                del amountdata['site']
                amountdata['amount'] = ammount
                json_result.append(amountdata)
        format_string += '"' + old_site + '":' + str(json_result)
        format_string = format_string.replace("\'", "\"")
        format_string = '{' + format_string + '}'

        json_data = format_string
        if json_data is not None:
            dataJsonArray = json.loads(json_data)
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        return result