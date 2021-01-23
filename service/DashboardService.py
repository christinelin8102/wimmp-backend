import json
import random
import logging
from datetime import datetime
from common.crmfilter import *
from service.dataSerializer.redis.RedisGet8CategorysDistributionService import RedisGet8CategorysDistributionService
from service.dataSerializer.redis.RedisGetPOTop10Service import RedisGetPOTop10Service
from service.dataSerializer.redis.RedisGetPurchaseAmountService import RedisGetPurchaseAmountService
from service.dataSerializer.redis.RedisGetVendorTop10Service import RedisGetVendorTop10Service
from service.dataSerializer.redis.RedisGetPaymentTermDistributionService import RedisGetPaymentTermDistributionService
from service.dataSerializer.GetDataService import GetDataService
from service.dataSerializer.DatabaseGetHeaderService import DatabaseGetHeaderService
from service.dataSerializer.DatabaseGetMonthlyPurchaseAmountService import DatabaseGetMonthlyPurchaseAmountService
from service.dataSerializer.DatabasePaymentTermService import DatabasePaymentTermService
from itertools import groupby
from operator import itemgetter
from service.utils.Organization import Organization
from service.utils.ServiceUtils import ServiceUtils
from service.dataSerializer.DatabaseGetPOTop10Service import DatabaseGetPOTop10Service
from service.dataSerializer.DatabaseVenderTop10Service import DatabaseVenderTop10Service
from service.dataSerializer.DatabaseGet8CategorysDistrbutionService import  DatabaseGet8CategorysDistrbutionService

logger = logging.getLogger(__name__)


class DashboardService:

    def getHeadr(self):
        service = DatabaseGetHeaderService()
        return service.serialize()

    def postMonthlyPurchaseAmountPerSite(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            service = DatabaseGetMonthlyPurchaseAmountService(req)
            return service.serialize()
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetPurchaseAmountService(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def postPaymentTermDistribution(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            service = DatabasePaymentTermService(req)
            return service.serialize()
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetPaymentTermDistributionService(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def postVenderTopTen(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            service = DatabaseVenderTop10Service(req)
            return service.serialize()
        else:
            ## go to redis
            '''redis'''
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetVendorTop10Service(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result
        testdata = []
        site = ['wks', 'wmy', 'wih', 'wmx', 'wok', 'wtz']
        testdata = []
        for sitename in site:
            vendorList = []
            for i in range(1, 11):
                vendorList.append({"vendorCode": "vendorCode" + str(i), "vendorName": "vendorName" + str(i),
                                   "amount": random.randint(100, 2000)})
            testdata.append({"site": sitename, "vendorList": vendorList})
        result = json.dumps(testdata)
        result = ApiResponse.emitSuccessOutput(json.loads(result))
        return result

    def getTopTenVendor(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        datetime_start = datetime.fromtimestamp(startdate)
        datetime_end = datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            ## go to sql
            '''sql'''
            sqlquery = '''select po.vendor_code  as vandercode, po.vendor_name  as vendername, sum(po.po_amount) as amount
                        from public."PURCHASE_ORDER" po
                        where po.vendor_code in (select vendor_code from public."PURCHASE_ORDER"
                        group by vendor_code order by sum(po_amount) desc limit 10)
                        group by po.vendor_code ,po.vendor_name
                        order by po.vendor_code'''
            data = GetDataService.getwistrondata(self, sqlquery)
            result = ApiResponse.emitSuccessOutput(data, msg="get data successfully.")
            return result
        else:
            ## go to redis
            '''redis'''
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetVendorTop10Service(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result
        testdata = []
        site = ['wks', 'wmy', 'wih', 'wmx', 'wok', 'wtz']
        testdata = []
        for sitename in site:
            vendorList = []
            for i in range(1, 11):
                vendorList.append({"vendorCode": "vendorCode" + str(i), "vendorName": "vendorName" + str(i),
                                   "amount": random.randint(100, 2000)})
            testdata.append({"site": sitename, "vendorList": vendorList})
        result = json.dumps(testdata)
        result = ApiResponse.emitSuccessOutput(json.loads(result))
        return result


    def getTopTenPO(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        datetime_start = datetime.fromtimestamp(startdate)
        datetime_end = datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            sqlquery = '''
            select po.vendor_code  as vandercode, po.vendor_name  as vendername, sum(po.po_amount) as amount
            from public."PURCHASE_ORDER" po
            where po.vendor_code in (select vendor_code from public."PURCHASE_ORDER"
            group by vendor_code order by sum(po_amount) desc limit 10)
            group by po.vendor_code ,po.vendor_name
            order by po.vendor_code
            '''
            data = GetDataService.getwistrondata(self, sqlquery)
            if data is None or data == []:
                return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            result = []
            format_string = ''
            column = ('poNo', 'poAmount', 'PCodeOrDeptCode', 'vendorName', 'prRemark')
            for row in data:
                result.append(dict(zip(column, row)))
            count = 1
            for amountdata in result:
                print(type(amountdata))
                if amountdata.get('prRemark') is None:
                    amountdata['prRemark'] = ''
                format_string = format_string + '\"' + str(count) + '\":' + str(amountdata) + ','
                count += 1
            format_string = format_string[:-1]
            format_string = format_string.replace("\'", "\"")
            format_string = '{' + format_string + '}'
            print(format_string)
            json_data = json.loads(format_string)
            return ApiResponse.emitSuccessOutput(json_data)

        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetPOTop10Service(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def get8Cate(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        datetime_start = datetime.fromtimestamp(startdate)
        datetime_end = datetime.fromtimestamp(enddate)
        dtStartStr = datetime_start.strftime('%Y-%m-%d')
        dtEndStr = datetime_end.strftime('%Y-%m-%d')

        #if False:
        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            sqlquery = '''SELECT paym as category ,sum(amnt) as amount FROM public.mmp_impc_wks
                        GROUP BY paym
                        order by sum(amnt) desc'''
            data = GetDataService.getwistrondata(self, sqlquery)
            print(data)
            if data is None:
                return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            result = []
            column = ('category', 'amount')
            for row in data:
                print(row)
                result.append(dict(zip(column, row)))
            print(result)
            result = json.dumps(result)
            json_data = json.loads(result)
            return ApiResponse.emitSuccessOutput(json_data)
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGet8CategorysDistributionService(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def getPaymentTermDistr(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        if False:
        #if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            self.getWistronPaymentTermDistribution()
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetPaymentTermDistributionService(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def getDashBoardHead(self):
        testdata = []
        BG = ['WSD', 'CSBG', 'CBG', 'SABU', 'SDBG', 'IBG', 'APB']
        for bg in BG:
            testdata.append({"bg": bg, "amount": random.randint(100, 2000)})
        result = json.dumps(testdata)
        return ApiResponse.emitSuccessOutput(json.loads(result))

    def getBgSitePlant(self):
        sqlquery = 'select plant."name" as plant , site."name" as site, bg."name" as bg' \
                   ' from public."PLANTS" plant inner join ' \
                   'public."SITES" site on plant.site_id  = site.id inner join public."BGS" bg on plant.bg_id  = bg.id'

        data = GetDataService.getwistrondata(self, sqlquery)
        if data is None:
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        oldbg = ''
        formatstring = ''
        checkstring = ''
        for bg, sitedata in groupby(data, key=itemgetter(2)):
            oldsite = ''
            formatstring += '{ "code" : "' + bg + '", "sites" : ['
            for d in sitedata:
                if oldsite != d[1] and oldsite != '':
                    formatstring += ']},'
                if bg + d[1] not in checkstring:
                    formatstring += '{ "code" : "' + d[1] + '", "plants" : ['
                    formatstring += '{ "code" : "' + d[0] + '" }'
                    oldsite = d[1]
                    checkstring += bg + d[1] + ','
                elif bg + d[1] in checkstring:
                    formatstring += ',{ "code" : "' + d[0] + '" }'
                    oldsite = d[1]
                    checkstring += bg + d[1] + ','
            if oldbg != bg or oldbg != '':
                formatstring += ']}]},'
            oldbg = bg
            print(formatstring)
        formatstring = formatstring[:-1]
        result = '[' + formatstring + ']'
        print(result)

        dataJsonArray = json.loads(result)

        jsonresult = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        return jsonresult
        pass

    def getRandInt(self):
        return random.randint(1, 300)

    def createBgSitePlantKey(self, bg, site, plan):
        keyList = []
        bgList = []
        siteList = []
        planList = []
        if bg.find(','):
            bgList = bg.split(',')
        else:
            bgList.append(bg)
        if site.find(','):
            siteList = site.split(',')
        else:
            siteList.append(site)
        if plan.find(','):
            planList = plan.split(',')
        else:
            planList.append(plan)
        for BG in bgList:
            for SITE in siteList:
                for PLAN in planList:
                    keyList.append(BG + '_' + SITE + '_' + PLAN)
        print(keyList)

        return keyList

    def postTopTenPO(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            service = DatabaseGetPOTop10Service(req)
            return service.serialize()
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGetPOTop10Service(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def postDbGet8CategorysDistrbution(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            service = DatabaseGet8CategorysDistrbutionService(req)
            return service.serialize()
        else:
            organization = Organization(bg, site, plan)
            key_list = organization.get_redis_format()
            service = RedisGet8CategorysDistributionService(key_list, startdate, enddate, vendor, reimburseTag)
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result
