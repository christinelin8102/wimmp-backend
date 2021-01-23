import json
# !/usr/bin/env python
import traceback

from cfg.debug import REDIS_CONNECT_PWD, REDIS_CONNECT_IP, LOGGING_FILENAME
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# User Home Page 4-1. Purchase Amount Chart
class RedisGetPurchaseAmountService(IDataSerializer):

    def __init__(self, key, start_score, end_score, vendor_type, reimburse_type):
        self.key = key
        self.s_score = start_score
        self.e_score = end_score
        self.db_no = 0
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type

        logger.debug("------RedisGetPurchaseAmountService Param: ")
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
            sumDataDict = {}  # key: yyyyMM+site, value: sum amount
            siteSet = set()
            dateSet = set()
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
                for data_json_tuple in result:    # result type is list
                    # data_json_tuple type is tuple
                    date_timestamp = datetime.fromtimestamp(data_json_tuple[1])
                    dateStr = date_timestamp.strftime('%Y%m')  # 日期yyyyMM
                    logger.debug("org timestamp: " + str(data_json_tuple[1]) + ", date_timestamp: " + str(date_timestamp) + ", dateStr: " + dateStr)

                    data = data_json_tuple[0]
                    rowDataDict = json.loads(data)
                    logger.debug("rowDataDic: " + str(rowDataDict))

                    site = rowDataDict['site']
                    if rowKey in rowDataDict.keys():
                        dataDict = rowDataDict[rowKey]

                        dataKey = site + "_" + dateStr
                        # logger.debug("dataKey: " + dataKey)
                        if dataKey in sumDataDict.keys():
                            sumDataDict[dataKey] += dataDict['amount']
                        else:
                            sumDataDict[dataKey] = dataDict['amount']

                    siteSet.add(site)   #取得所有的site
                    dateSet.add(dateStr) # 取得所有yyyyMM

            logger.debug("===siteSet : "+str(siteSet))
            logger.debug("===dateSet : " + str(dateSet))
            logger.debug("===sum data count: " + str(sum_count))

            # 回傳API Json
            logger.debug("sumDataDic: " + str(sumDataDict))
            if bool(sumDataDict):  # 若Dict有資料

                #排序日期
                dateSet_sort = sorted(dateSet)

                #根據site 和 date new 所有的殼
                mainObject = {}
                for siteSet_key in siteSet:
                    mainObject[siteSet_key] = []
                    for dateSet_key in dateSet_sort:
                        subObject = {}
                        subObject['date'] = dateSet_key
                        sumDataDict_key = siteSet_key + "_" + dateSet_key
                        if sumDataDict_key in sumDataDict:
                            subObject['amount'] = sumDataDict[sumDataDict_key]
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

