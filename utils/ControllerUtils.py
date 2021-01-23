import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from enumClass.IsIgnoreType import IsIgnoreVendor
from enumClass.ReimburseType import ReimburseType

logger = logging.getLogger(__name__)


class requestBasicBody:
    def __init__(self, bg, site, plant, startdate, enddate):
        self.bg = bg
        self.site = site
        self.plant = plant
        self.startdate = startdate
        self.enddate = enddate


class requestbody(requestBasicBody):
    def __init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate):
        requestBasicBody.__init__(self, bg, site, plant, startdate, enddate)
        self.vendor = vendor
        self.reimburseTag = reimburseTag


class requestbodypage(requestBasicBody):
    def __init__(self, paymentterm, processTag, bg, site, plant,
                 startdate, enddate, currentPage, pageSize, pageNo, search_key):
        requestBasicBody.__init__(self, bg, site, plant, startdate, enddate)
        self.paymentterm = paymentterm
        self.processTag = processTag
        self.currentPage = currentPage
        self.pageSize = pageSize
        self.pageNo = pageNo
        self.search_key = search_key


class requestDailyMgtTableBodyByPage_poMain(requestbody):
    def __init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate,
                 pageSize, pageNo, sort, filter):  # sort and filter data type: 物件的list
        requestbody.__init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate)
        self.pageSize = pageSize
        self.pageNo = pageNo
        self.sort = sort
        self.filter = filter

class requestDailyMgtTableBodyByPage_subPo(requestDailyMgtTableBodyByPage_poMain):
    def __init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate,
                 pageSize, pageNo, sort, filter, anyParam):
        requestDailyMgtTableBodyByPage_poMain.__init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate,
                                                       pageSize, pageNo, sort, filter)
        # anyParam : pCode or vendorName or categories or paymentTerm or poNo
        self.anyParam = anyParam


class requestDailyMgtButton(requestbody):
    def __init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate, anyParam):
        requestbody.__init__(self, vendor, reimburseTag, bg, site, plant, startdate, enddate)
        # anyParam : pCode or vendorName or categories or paymentTerm or poNo
        self.anyParam = anyParam

def basic_handleRequestBody(data):
    endD = datetime.now()
    startD = endD - relativedelta(years=1)
    # logger.debug("test endD = "+ str(endD))
    bg = data.get('bg', None)
    site = data.get('site', None)
    plant = data.get('plant', None)
    period = data.get('period', None)
    if period:
        startdate = period.get('startdate', startD)
        enddate = period.get('enddate', endD)

    return requestBasicBody(bg, site, plant, startdate, enddate)


def basic_handleRequestBody_WithVendorAndReimburse(data):
    basicVo = basic_handleRequestBody(data)
    vendor = data.get('vendor', None)
    if vendor is True:
        vendor = IsIgnoreVendor.YES.value
    else:
        vendor = IsIgnoreVendor.NO.value
    reimburse = data.get('reimburse', True)
    nonreimburse = data.get('nonreimburse', True)
    if reimburse:
        if nonreimburse:
            reimburseTag = ReimburseType.ALL.value
        else:
            reimburseTag = ReimburseType.YES.value
    elif nonreimburse:
        reimburseTag = ReimburseType.NO.value
    else:
        return "reimburse nonreimburse 不得皆為False"

    return requestbody(vendor, reimburseTag,
                       basicVo.bg, basicVo.site, basicVo.plant,
                       basicVo.startdate, basicVo.enddate)

def basic_handleRequestBody_DailyManagementTable(data):
    basicVo = basic_handleRequestBody_WithVendorAndReimburse(data)
    sort = data.get("sort", None)
    filter = data.get("filter", None)
    pageSize = data.get("pageSize", 10)
    pageNo = data.get("pageNo", 1)

    return requestDailyMgtTableBodyByPage_poMain(basicVo.vendor, basicVo.reimburseTag,
                                                           basicVo.bg, basicVo.site, basicVo.plant, basicVo.startdate,
                                                           basicVo.enddate,
                                                           pageSize, pageNo, sort, filter)

class ControllerUtils:

    @staticmethod
    def handleRequestBody(data):
        return basic_handleRequestBody_WithVendorAndReimburse(data)

    @staticmethod
    def handleRequestBodyExcept(data):

        basicVo = basic_handleRequestBody(data)

        paymentterm = data.get('paymentterm', None)
        process = data.get('process', True)
        notprocess = data.get('notprocess', True)
        if process:
            if notprocess:
                processTag = 0
            else:
                processTag = 1
        elif notprocess:
            processTag = 2
        else:
            return "process notprocess 不得皆為False"

        currentPage = data.get("currentPage", 1)
        if currentPage is not None and currentPage != "":
            currentPage = int(currentPage)
        pageSize = data.get("pageSize", 10)
        if pageSize is not None and pageSize != '':
            pageSize = int(pageSize)
        pageNo = data.get('pageNo', 1)
        if pageNo is not None and pageNo != '':
            pageNo = int(pageNo)
        search_key = data.get("search_key")
        if currentPage is None or currentPage == "":
            currentPage = 1
        if pageSize is None or pageSize == "":
            pageSize = 10

        return requestbodypage(paymentterm, processTag, basicVo.bg, basicVo.site, basicVo.plant,
                               basicVo.startdate, basicVo.enddate,
                               currentPage, pageSize, pageNo, search_key)

    @staticmethod
    def handleRequestDailyMgtTableBody_Top10(data):
        return basic_handleRequestBody_DailyManagementTable(data)

    @staticmethod
    def handleRequestDailyMgtTableBody_purchaseOrPoOrPoline(data):
        basicVo = basic_handleRequestBody_DailyManagementTable(data)
        anyParam = None

        pCode = data.get("pCode", None)
        poNo = data.get("poNo", None)
        vendorName = data.get("vendorName", None)
        categories = data.get("categories", None)
        paymentTerm = data.get("paymentCode", None)

        if pCode is not None:   # For p code top 10 PurchasePerSite and PO
            anyParam = pCode
        elif poNo is not None:   # For p code top 10
            anyParam = poNo
        elif vendorName is not None:   # For vendor top 10 PurchasePerSite and PO
            anyParam = vendorName
        elif categories is not None:   # For 8 categories PurchasePerSite and PO
            anyParam = categories
        elif paymentTerm is not None:   # For payment term PurchasePerSite and PO
            anyParam = paymentTerm

        return requestDailyMgtTableBodyByPage_subPo(basicVo.vendor, basicVo.reimburseTag,
                                                  basicVo.bg, basicVo.site, basicVo.plant, basicVo.startdate,
                                                  basicVo.enddate, basicVo.pageSize, basicVo.pageNo,
                                                  basicVo.sort, basicVo.filter, anyParam)
