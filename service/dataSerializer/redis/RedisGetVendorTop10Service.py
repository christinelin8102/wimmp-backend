import json
# !/usr/bin/env python
import traceback

from cfg.debug import REDIS_CONNECT_PWD, REDIS_CONNECT_IP, LOGGING_FILENAME
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# User Home Page 4-4. Vender top 10 Chart
class RedisGetVendorTop10Service(IDataSerializer):

    def __init__(self, key, start_score, end_score, vendor_type, reimburse_type):
        self.key = key
        self.s_score = start_score
        self.e_score = end_score
        self.db_no = 3
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type

        logger.debug("------RedisGetVendorTop10Service Param: ")
        logger.debug("key: " + str(self.key))  # key List
        logger.debug("score: " + str(self.s_score) + " ~ " + str(self.e_score))
        logger.debug("dbNo: " + str(self.db_no))
        logger.debug("isIgnoreVendor: " + self.vendor_type)
        logger.debug("Reimburse: " + str(self.reimburse_type))

        connector = RedisConnector(REDIS_CONNECT_IP, None, REDIS_CONNECT_PWD, 6379, self.db_no)
        connector = connector.getConnectionInfo()
        self._connector = connector

    def serialize(self):
        apiJsonArr = {}
        try:
            sum_count = 0
            sumDataDict = {}  # key: site_vendorCode, value: sum amount
            siteSet = set()
            sumVendorDict = {}  # key: vendorCode_vendorName, value: sum amount
            for theKey in self.key:
                result = self._connector.zrangebyscore(theKey, self.s_score, self.e_score, withscores=True)
                logger.debug("====================")
                logger.debug("Key: " + theKey + ", zrangebyscore result: " + str(result))
                count = self._connector.zcount(theKey, self.s_score, self.e_score)
                logger.debug("Key: " + theKey + ", row data count: " + str(count))
                sum_count += count

                # 解析Redis Json Value
                rowKey = str(self.reimburse_type) + self.vendor_type
                logger.debug("rowKey: " + rowKey)
                for data_json_tuple in result:  # result type is list
                    # data_json_tuple type is tuple
                    date_timestamp = datetime.fromtimestamp(data_json_tuple[1])
                    dateStr = date_timestamp.strftime('%Y%m')  # 日期yyyyMM
                    logger.debug("date_timestamp: " + str(date_timestamp))

                    data = data_json_tuple[0]
                    rowDataDict = json.loads(data)
                    logger.debug("rowDataDic: " + str(rowDataDict))

                    site = rowDataDict['site']
                    if rowKey in rowDataDict.keys():
                        dataList = rowDataDict[rowKey]
                        for dataDict in dataList:
                            vendorCode = dataDict['vendorCode']
                            vendorName = dataDict['vendorName']

                            dataKey = site + "_" + vendorCode
                            # logger.debug("dataKey: " + dataKey)
                            if dataKey in sumDataDict.keys():
                                sumDataDict[dataKey] += dataDict['amount']
                            else:
                                sumDataDict[dataKey] = dataDict['amount']

                            vendorKey = vendorCode + "_" + vendorName
                            if vendorKey in sumVendorDict.keys():
                                sumVendorDict[vendorKey] += dataDict['amount']
                            else:
                                sumVendorDict[vendorKey] = dataDict['amount']

                    siteSet.add(site)  # 取得所有的site

            logger.debug("===siteSet : " + str(siteSet))
            logger.debug("===sum data count: " + str(sum_count))

            # 回傳API Json
            logger.debug("sumDataDic: " + str(sumDataDict))
            logger.debug("sumVendorDict: " + str(sumVendorDict))
            if bool(sumDataDict):  # 若Dict有資料
                apiJsonList = []  # 最外層Array

                venderbDict_sorted_list = sorted(sumVendorDict.items(), key=lambda x: x[1], reverse=True)  # 降序排序
                logger.debug("vendebDict_sorted_list = " + str(venderbDict_sorted_list))  # vendebDict_sorted data type is tuple

                vendorlist_len = 0 # length長度
                if len(venderbDict_sorted_list) >= 10:
                    vendorlist_len = 10
                elif 0 < len(venderbDict_sorted_list) < 10:
                    vendorlist_len = len(venderbDict_sorted_list)

                # 先new所有的site
                mainObject = {}
                for siteSet_key in siteSet:
                    mainObject[siteSet_key] = []
                    # 再new前10名vendor
                    if len(venderbDict_sorted_list) > 0:
                        for vendor_tuple in venderbDict_sorted_list[0:vendorlist_len]:  # 取前10名
                            vendorSplit = vendor_tuple[0].split("_", 1)
                            subObject = {}
                            subObject['vendorCode'] = vendorSplit[0]
                            subObject['vendorName'] = vendorSplit[1]
                            sumDataDict_key = siteSet_key + "_" + vendorSplit[0]
                            logger.debug("sumDataDict_key : " + sumDataDict_key)
                            if sumDataDict_key in sumDataDict.keys():
                                subObject['amount'] = sumDataDict[sumDataDict_key]
                                logger.debug("sumDataDict data : " + str(sumDataDict[sumDataDict_key]))
                            else:
                                subObject['amount'] = 0
                            mainObject[siteSet_key].append(subObject)

                apiJsonArr = json.dumps(mainObject, ensure_ascii=False)
                logger.info("dict轉JSON: " + str(apiJsonArr))
            else:
                apiJsonArr = None

        except Exception as ex:
            logger.error("Fail! Reason: " + traceback.format_exc())
            apiJsonArr = None

        finally:
            return apiJsonArr