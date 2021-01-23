import json
import logging
from operator import itemgetter
from itertools import groupby

from common.crmfilter import *
from enumClass.DailyManagementPageTableCategoriesType import DailyManagementPageTableCategoriesType
from service.dataSerializer.dailyManagement.projectCode.DBPcodeListSQL import DBPcodeListSQL
from service.dataSerializer.redis.RedisGetPCodeTop10BarService import RedisGetPCodeTop10BarService
from service.dataSerializer.redis.RedisGetVendorTop10Service import RedisGetVendorTop10Service
from service.dataSerializer.DatabaseGetTopTenVendorChartService import DatabaseGetTopTenVendorChartService
from service.dataSerializer.dailyManagement.projectCode.DBPcodeListButton import DBPcodeListButton
from service.utils.Organization import Organization
from service.dataSerializer.DatabaseGetTopTenVendorListService import DatabaseGetTopTenVendorListService
from service.dataSerializer.DatabaseGetVendorPurchaseListService import DatabaseGetVendorPurchaseListService
from service.utils.ServiceUtils import ServiceUtils
from service.utils.GenerateQueryFilter import GenerateQueryFilter
from service.dataSerializer.dailyManagement.projectCode.PurchaseAmountPerSite import PurchaseAmountPerSite
from service.dataSerializer.dailyManagement.projectCode.PurchaseOrderList import PurchaseOrderList
from service.dataSerializer.dailyManagement.projectCode.PurchaseOrderLineList import PurchaseOrderLineList
from service.dataSerializer.dailyManagement.categories.CategoriesAmount import CategoriesAmount
logger = logging.getLogger(__name__)


class DashboardDailyMgtService:

    def exportDataBycode(self, req, p_code):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate

        service = DBPcodeListButton(pcode=p_code, bg_list=bg, site_list=site, plant_list=plant, start_score=startdate,
                                    end_score=enddate, reimburse_type=reimburseTag, vendor_type=vendor)
        return service.serialize()

    def getTopTenPCode(self, req):

        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate

        organization = Organization(bg, site, plant)
        key_list = organization.get_redis_format()

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            logger.info("超過一年內查詢區間 DB")
            # TODO(Christine) 撈取DB資料
        else:
            ## go to redis
            logger.info("一年內查詢區間 redis")
            '''redis'''
            service = RedisGetPCodeTop10BarService(key_list, startdate, enddate, vendor,
                                                   reimburseTag)  # 1598889600 ~ 1609171200
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def getTopTenList(self, req, pageType):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate
        pageSize = req.pageSize
        pageNo = req.pageNo
        sort = req.sort
        filter = req.filter

        if bg is not None: bg = bg.split(",")
        if site is not None:  site = site.split(",")
        if plant is not None: plant = plant.split(",")

        logger.debug("Param----------------")
        logger.debug("vendor = " + str(vendor))
        logger.debug("reimburseTag = " + str(reimburseTag))
        logger.debug("bg = " + str(bg))
        logger.debug("site = " + str(site))
        logger.debug("plant = " + str(plant))
        logger.debug("startdate = " + str(startdate))
        logger.debug("enddate = " + str(enddate))
        logger.debug("pageSize = " + str(pageSize))
        logger.debug("pageNo = " + str(pageNo))
        logger.debug("sort = " + str(sort))
        logger.debug("filter = " + str(filter))
        dictData = {}

        if pageType == DailyManagementPageTableCategoriesType.PCODE_TOP10:
            service = DBPcodeListSQL(bg, site, plant, startdate, enddate, vendor, reimburseTag, pageSize, pageNo,
                                     sort, filter)
            result = service.serialize()
            dictData = result

        if pageType == DailyManagementPageTableCategoriesType.VENDOR_TOP10:
            logger.debug("===VENDOR_TOP10 List")
            # TODO()
            service = DatabaseGetTopTenVendorListService(bg, site, plant, startdate, enddate, vendor,
                                                         reimburseTag, pageSize, pageNo)  # 1598889600 ~ 1609171200
            dictData = service.serialize()

        if pageType == DailyManagementPageTableCategoriesType.EIGHTCATEGORIES:
            generate = GenerateQueryFilter(req)
            ft = generate.generate_header_filter()
            service = CategoriesAmount(ft, req.anyParam)
            data = service.serialize()
            dictData["totalPage"] = None
            dictData["totalCount"] = None
            dictData["data"] = data

        if pageType == DailyManagementPageTableCategoriesType.PAYMENTTERM:
            logger.debug("===PAYMENTTERM List")
            # TODO()

        totalPage = dictData["totalPage"]
        totalCount = dictData["totalCount"]
        json_data = dictData["data"]

        if json_data is not None:
            # TODO: 需要修改，不需要轉一次json string，然後再轉object
            dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.",
                                                   pageSize=pageSize, pageNo=pageNo,
                                                   totalPage=totalPage, totalCount=totalCount)
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")

        return result

    def getSubTable(self, req, pageType):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate
        pageSize = req.pageSize
        pageNo = req.pageNo
        sort = req.sort
        filter = req.filter

        if bg is not None: bg = bg.split(",")
        if site is not None: site = site.split(",")
        if plant is not None: plant = plant.split(",")

        logger.debug("Param----------------")
        logger.debug("vendor = " + str(vendor))
        logger.debug("reimburseTag = " + str(reimburseTag))
        logger.debug("bg = " + str(bg))
        logger.debug("site = " + str(site))
        logger.debug("plant = " + str(plant))
        logger.debug("startdate = " + str(startdate))
        logger.debug("enddate = " + str(enddate))
        logger.debug("pageSize = " + str(pageSize))
        logger.debug("pageNo = " + str(pageNo))
        logger.debug("sort = " + str(sort))
        logger.debug("filter = " + str(filter))

        response_data = {}
        if pageType == DailyManagementPageTableCategoriesType.PCODETOP10_PUCHASE_PER_SITE:
            project_code = req.anyParam
            generate = GenerateQueryFilter(req)
            ft = generate.generate_header_filter()
            service = PurchaseAmountPerSite(ft, project_code, pageNo, pageSize)
            total, pages, data = service.serialize()
            response_data["totalPage"] = pages
            response_data["totalCount"] = total
            response_data["data"] = data
        if pageType == DailyManagementPageTableCategoriesType.PCODE_PO_LIST:
            generate = GenerateQueryFilter(req)
            ft = generate.generate_header_filter()
            service = PurchaseOrderList(ft, req.anyParam, pageNo, pageSize)
            total, pages, data = service.serialize()
            response_data["totalPage"] = pages
            response_data["totalCount"] = total
            response_data["data"] = data

        if pageType == DailyManagementPageTableCategoriesType.PO_LINE_LIST:
            generate = GenerateQueryFilter(req)
            ft = generate.generate_header_filter()
            service = PurchaseOrderLineList(ft, req.anyParam, pageNo, pageSize)
            total, pages, data = service.serialize()
            response_data["totalPage"] = pages
            response_data["totalCount"] = total
            response_data["data"] = data
        if pageType == DailyManagementPageTableCategoriesType.VENDORTOP10_PUCHASE_PER_SITE:
            logger.debug("===top 10 vendor purchase")
            vendorName = req.anyParam
            logger.debug("vendorName = " + str(vendorName))
            # TODO() 待接DB資料
            service = DatabaseGetVendorPurchaseListService(bg, site, plant, startdate, enddate, vendor,
                                                           reimburseTag, vendorName, pageSize,
                                                           pageNo)  # 1598889600 ~ 1609171200
            dictData = service.serialize()
        if pageType == DailyManagementPageTableCategoriesType.VENDORTOP10_PO:
            logger.debug("===top 10 vendor po")
            vendorName = req.anyParam
            logger.debug("vendorName = " + str(vendorName))
            # TODO() 待接DB資料
        if pageType == DailyManagementPageTableCategoriesType.EIGHTCATEGORIES_PUCHASE_PER_SITE:
            logger.debug("===8 categories purchase")
            categories = req.anyParam
            logger.debug("categories = " + str(categories))
            # TODO() 待接DB資料
        if pageType == DailyManagementPageTableCategoriesType.EIGHTCATEGORIES_PO:
            logger.debug("===8 categories po")
            categories = req.anyParam
            logger.debug("categories = " + str(categories))
            # TODO() 待接DB資料
        if pageType == DailyManagementPageTableCategoriesType.PAYMENTTERM_PUCHASE_PER_SITE:
            logger.debug("===paymentTerm purchase")
            paymentTerm = req.anyParam
            logger.debug("paymentCode = " + str(paymentTerm))
            # TODO() 待接DB資料
        if pageType == DailyManagementPageTableCategoriesType.PAYMENTTERM_PO:
            logger.debug("===paymentTerm purchase")
            paymentTerm = req.anyParam
            logger.debug("paymentCode = " + str(paymentTerm))
            # TODO() 待接DB資料


        totalPage = response_data["totalPage"]
        totalCount = response_data["totalCount"]
        json_data = response_data["data"]

        if json_data is not None:
            json_array = json.loads(json_data)  # JSON字串轉Python dict
            result = ApiResponse.emitSuccessOutput(json_array, msg="get data successfully.",
                                                   pageSize=pageSize, pageNo=pageNo,
                                                   totalPage=totalPage, totalCount=totalCount)
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")

        return result

    def getTopTenVendorChart(self, req):

        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate

        organization = Organization(bg, site, plant)
        bg = organization.bg
        site = organization.site
        plant = organization.plant
        key_list = organization.get_redis_format()

        if ServiceUtils.isMoreThanOneYear(startdate, enddate):
            logger.info("超過一年內查詢區間 DB")
            # TODO() 撈取DB資料
            service = DatabaseGetTopTenVendorChartService(bg, site, plant, startdate, enddate, vendor,
                                                          reimburseTag)  # 1598889600 ~ 1609171200
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                resultArray = []

                dataJsonArray.sort(key=itemgetter('site'))
                groupArray = groupby(dataJsonArray, itemgetter('site'))
                for key, group in groupArray:
                    vendorList = []
                    for g in group:
                        vendorList.append(g)
                    resultDic = {"site": key, "vendorList": vendorList}
                    resultArray.append(resultDic)

                result = ApiResponse.emitSuccessOutput(resultArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

        else:
            ## go to redis
            logger.info("一年內查詢區間 redis")
            '''redis'''
            service = RedisGetVendorTop10Service(key_list, startdate, enddate, vendor,
                                                 reimburseTag)  # 1598889600 ~ 1609171200
            json_data = service.serialize()
            if json_data is not None:
                dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
                result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
            else:
                result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
            return result

    def getTopTenVendorList(self, req):
        vendor = req.vendor
        reimburseTag = req.reimburseTag
        bg = req.bg
        site = req.site
        plant = req.plant
        startdate = req.startdate
        enddate = req.enddate

        organization = Organization(bg, site, plant)
        bg = organization.bg
        site = organization.site
        plant = organization.plant
        key_list = organization.get_redis_format()

        logger.info("超過一年內查詢區間 pass")
        # TODO() 撈取DB資料
        service = DatabaseGetTopTenVendorListService(bg, site, plant, startdate, enddate, vendor,
                                                     reimburseTag)  # 1598889600 ~ 1609171200
        json_data = service.serialize()
        if json_data is not None:
            dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        return result


    # fortest

    def getVendorPurchase(self, vendor, reimburseTag, bg, site, plant, startdate, enddate, vendorName):
        # vendor = self.vendor
        # reimburseTag = self.reimburseTag
        # bg = self.bg
        # site = self.site
        # plant = self.plant
        # startdate = self.startdate
        # enddate = self.enddate

        organization = Organization(bg, site, plant)
        bg = organization.bg
        site = organization.site
        plant = organization.plant
        key_list = organization.get_redis_format()

        logger.info("超過一年內查詢區間 pass")
        # TODO() 撈取DB資料
        service = DatabaseGetVendorPurchaseListService(bg, site, plant, startdate, enddate, vendor,
                                                       reimburseTag, vendorName)  # 1598889600 ~ 1609171200
        json_data = service.serialize()
        if json_data is not None:
            dataJsonArray = json.loads(json_data)  # JSON字串轉Python dict
            result = ApiResponse.emitSuccessOutput(dataJsonArray, msg="get data successfully.")
        else:
            result = ApiResponse.emitErrorOutput(E_QUERY_FAIL, "查無資料", "no data")
        return result
