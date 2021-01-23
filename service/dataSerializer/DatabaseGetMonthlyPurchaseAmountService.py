import logging
import json
from service.connector.PostgresqlConnector import PostgresqlConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from utils.ApiResponse import ApiResponse, E_QUERY_FAIL
from service.dataSerializer.GetDataService import GetDataService
from model.Plant import ObjPlant
from model.Site import ObjSite
from model.BG import ObjBG
from model.database import db
import datetime
from itertools import groupby
from operator import itemgetter

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


class DatabaseGetMonthlyPurchaseAmountService(IDataSerializer):

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

        logger.debug("------DatabaseGetMonthlyPurchaseAmountService Param: ")
        logger.debug("bg: " + str(bg))
        logger.debug("site: " + str(site))
        logger.debug("plan: " + str(plant))
        logger.debug("score: " + str(dtStartStr) + " ~ " + str(dtEndStr))

        queryTyoe = 0
        if bg == '' and site == '' and plant == '':
            queryTyoe = 1
        if queryTyoe == 1:
            sqlquery = 'select mmp_site as site, to_char(po_date , \'YYYY/MM\') as date, sum(po_line_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'inner join public."PURCHASE_ORDER_DETAIL" pod ' \
                       'on po.po_no = pod.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' ' \
                       'and charge_plant_code is not null ' \
                       'and mmp_bg is not null and mmp_site is not null ' \
                       'group by mmp_site, to_char(po_date, \'YYYY/MM\')' \
                       'order by mmp_site, to_char(po_date, \'YYYY/MM\')'
        else:
            sqlquery = 'select mmp_site as site, to_char(po_date , \'YYYY/MM\') as date, sum(po_line_amount) as amount ' \
                       'from public."PURCHASE_ORDER" po ' \
                       'inner join public."PURCHASE_ORDER_DETAIL" pod ' \
                       'on po.po_no = pod.po_no ' \
                       'where po_date between \'' + dtStartStr + '\' and \'' + dtEndStr + '\' '
            if plant != '':
                sqlquery += 'and charge_plant_code in (' + str(plant.split(',')).replace('[','').replace(']','') + ')'
            if bg != '':
                sqlquery += 'and mmp_bg in (' + str(bg.split(',')).replace('[', '').replace(']', '') + ')'
            if site != '':
                sqlquery += 'and mmp_site in (' + str(site.split(',')).replace('[','').replace(']','') + ')'

            sqlquery += 'group by mmp_site, to_char(po_date, \'YYYY/MM\') order by mmp_site, to_char(po_date, \'YYYY/MM\')'
        print(sqlquery)
        data = GetDataService.getdata(self, sqlquery)
        if data is None or data == []:
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        result = []
        json_result = []
        format_string = ''
        column = ('site', 'date', 'amount')
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