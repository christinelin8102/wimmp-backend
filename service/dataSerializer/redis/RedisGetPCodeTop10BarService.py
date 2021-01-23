import json
import logging
# !/usr/bin/env python
import traceback

from cfg.debug import REDIS_CONNECT_PWD, REDIS_CONNECT_IP, LOGGING_FILENAME
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from datetime import datetime

logger = logging.getLogger(__name__)

# Daily Management 1. Top 10 P Code Chart
class RedisGetPCodeTop10BarService(IDataSerializer):

    def __init__(self, key, start_score, end_score, vendor_type, reimburse_type):
        self.key = key
        self.s_score = start_score
        self.e_score = end_score
        self.db_no = 5
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type

        logger.debug("------Param: ")
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
            sumDataDict = {}  # key: site_pCode, value: sum amount
            siteSet = set()
            sumPCodeDict = {}  # key: pCode, value: sum amount
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
                    # dateStr = date_timestamp.strftime('%Y%m')  # 日期yyyyMM
                    logger.debug("date_timestamp: " + str(date_timestamp))

                    data = data_json_tuple[0]
                    rowDataDict = json.loads(data)
                    logger.debug("rowDataDic: " + str(rowDataDict))

                    site = rowDataDict['site']
                    if rowKey in rowDataDict.keys():
                        dataList = rowDataDict[rowKey]
                        for dataDict in dataList:
                            pCode = dataDict['pCode']

                            dataKey = site + "_" + pCode
                            # logger.debug("dataKey: " + dataKey)
                            if dataKey in sumDataDict.keys():
                                sumDataDict[dataKey] += dataDict['amount']
                            else:
                                sumDataDict[dataKey] = dataDict['amount']

                            if pCode in sumPCodeDict.keys():
                                sumPCodeDict[pCode] += dataDict['amount']
                            else:
                                sumPCodeDict[pCode] = dataDict['amount']

                    siteSet.add(site)  # 取得所有的site

            logger.debug("===siteSet : " + str(siteSet))
            logger.debug("===sum data count: " + str(sum_count))

            # 回傳API Json
            logger.debug("sumDataDic: " + str(sumDataDict))
            logger.debug("sumPCodeDict: " + str(sumPCodeDict))
            if bool(sumDataDict):  # 若Dict有資料

                pcodebDict_sorted_list = sorted(sumPCodeDict.items(), key=lambda x: x[1], reverse=True)  # 降序排序
                logger.debug("vendebDict_sorted_list = " + str(
                    pcodebDict_sorted_list))  # pcodebDict_sorted_list data type is tuple

                pCodelist_len = 0  # length長度
                if len(pcodebDict_sorted_list) >= 10:
                    pCodelist_len = 10
                elif 0 < len(pcodebDict_sorted_list) < 10:
                    pCodelist_len = len(pcodebDict_sorted_list)

                # 先new所有的site
                mainObject = {}
                for siteSet_key in siteSet:
                    mainObject[siteSet_key] = []
                    # 再new前10名pCode
                    if len(pcodebDict_sorted_list) > 0:
                        for pCode_tuple in pcodebDict_sorted_list[0:pCodelist_len]:  # 取前10名
                            pCodeSplit = pCode_tuple[0].split("_", 1)
                            subObject = {}
                            subObject['pCode'] = pCodeSplit[0]
                            sumDataDict_key = siteSet_key + "_" + pCodeSplit[0]
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

