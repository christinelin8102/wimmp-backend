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


class DatabaseGet8CategorysDistrbutionService(IDataSerializer):

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

        logger.debug("------DatabaseGet8CategorysDistrbutionService Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))

        queryTyoe = 0
        if bg == '' and site == '' and plant == '':
            queryTyoe = 1
        if queryTyoe == 1:
            sqlquery = 'select pod.category as category, poc.mmp_charge as percent,sum(po_line_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'inner join public."PURCHASE_ORDER_DETAIL" pod ' \
                       'on po.po_no = pod.po_no ' \
                       'inner join public."PURCHASE_ORDER_CHARGE" poc ' \
                       'on po.po_no = poc.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' ' \
                       'group by pod.category, poc.mmp_charge '\
                       'order by pod.category, poc.mmp_charge'
        else:
            sqlquery = 'select pod.category as category, poc.mmp_charge as percent,  sum(po_line_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'inner join public."PURCHASE_ORDER_DETAIL" pod ' \
                       'on po.po_no = pod.po_no ' \
                       'inner join public."PURCHASE_ORDER_CHARGE" poc ' \
                       'on po.po_no = poc.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' '
            if plant != '':
                sqlquery += 'and charge_plant_code in (' + str(plant.split(',')).replace('[','').replace(']','') + ')'
            if bg != '':
                sqlquery += 'and mmp_bg in (' + str(bg.split(',')).replace('[', '').replace(']', '') + ')'
            if site != '':
                sqlquery += 'and mmp_site in (' + str(site.split(',')).replace('[','').replace(']','') + ')'

            sqlquery += 'group by pod.category, poc.mmp_charge order by pod.category, poc.mmp_charge '
        print(sqlquery)
        data = GetDataService.getdata(self, sqlquery)
        print(data)
        if data == []:
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        result = []
        column = ('category', 'percent', 'amount')
        for row in data:
            print(row)
            result.append(dict(zip(column, row)))
        print(result)
        ostr = ''
        for index, term in enumerate(data):
            if index + 1 < len(data):
             ostr += '"' + term[0] + '" : ' + '{ "percent" : "' + str(term[1]) + '" , "amount" : "' + str(term[
                2]) + '" },'
            elif index + 1 == len(data):
                ostr += '"' + term[0] + '" : ' + '{ "percent" : "' + str(term[1]) + '" , "amount" : "' + str(term[
                                                                                                          2]) + '" }'
        strjson = '{' + ostr + '}'
        print(strjson)
        json_data = strjson
        if json_data is not None:
            dataJsonArray = json.loads(json_data)
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        return result
