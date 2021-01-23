import json
# !/usr/bin/env python
import traceback

from cfg.debug import REDIS_CONNECT_PWD, REDIS_CONNECT_IP, LOGGING_FILENAME
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# User Home Page 4-5. PO top 10 Chart
class RedisGetPOTop10Service(IDataSerializer):

    def __init__(self, key, start_score, end_score, vendor_type, reimburse_type):
        self.key = key
        self.s_score = start_score
        self.e_score = end_score
        self.db_no = 4
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type

        logger.debug("------RedisGetPOTop10Service Param: ")
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
            sumDataDict = {}  # key: poNo, value: po data
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

                    if rowKey in rowDataDict.keys():
                        dataList = rowDataDict[rowKey]
                        for dataDict in dataList:
                            poNo = dataDict['poNo']
                            amount = dataDict['amount']
                            poOrDeptCode = dataDict['poOrDeptCode']
                            vendorName = dataDict['vendorName']
                            prRemark = dataDict['prRemark']

                            dataKey = poNo
                            if dataKey in sumDataDict.keys():
                                sumDataDict[dataKey]['amount'] += dataDict['amount']
                            else:
                                sumDataDict[dataKey] = dataDict['amount']
                                dataDict = {}
                                dataDict['amount'] = amount
                                dataDict['poOrDeptCode'] = poOrDeptCode
                                dataDict['vendorName'] = vendorName
                                dataDict['prRemark'] = prRemark
                                sumDataDict[dataKey] = dataDict

            logger.debug("===sum data count: " + str(sum_count))

            # 回傳API Json
            logger.debug("sumDataDic: " + str(sumDataDict))
            if bool(sumDataDict):  # 若Dict有資料
                # 依PO amount排序
                sumDataDict_sorted_list = sorted(sumDataDict.items(), key=lambda x: x[1]['amount'], reverse=True)  # 降序排序
                logger.debug("sumDataDict_sorted_list = " + str(sumDataDict_sorted_list))  # sumDataDict_sorted_list data type is tuple

                sumDatalist_len = 0  # length長度
                if len(sumDataDict_sorted_list) >= 10:
                    sumDatalist_len = 10
                elif 0 < len(sumDataDict_sorted_list) < 10:
                    sumDatalist_len = len(sumDataDict_sorted_list)

                # 組Json檔
                mainObject = {}
                if len(sumDataDict_sorted_list) > 0:
                    rank_count = 1
                    for data_tuple in sumDataDict_sorted_list[0:sumDatalist_len]:  # 取前10名
                        dataDict = data_tuple[1]
                        mainObject[rank_count] = {}
                        mainObject[rank_count]['poNo'] = data_tuple[0]
                        mainObject[rank_count]['poAmount'] = dataDict['amount']
                        mainObject[rank_count]['poOrDeptCode'] = dataDict['poOrDeptCode']
                        mainObject[rank_count]['vendorName'] = dataDict['vendorName']
                        mainObject[rank_count]['prRemark'] = dataDict['prRemark']
                        rank_count += 1

                apiJsonArr = json.dumps(mainObject, ensure_ascii=False)
                logger.info("dict轉JSON: " + str(apiJsonArr))
            else:
                apiJsonArr = None

        except Exception as ex:
            logger.error("Fail! Reason: {}" + traceback.format_exc())
            apiJsonArr = None

        finally:
            return apiJsonArr
