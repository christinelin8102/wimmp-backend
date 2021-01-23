import json
# !/usr/bin/env python
import traceback

from cfg.debug import REDIS_CONNECT_PWD, REDIS_CONNECT_IP, LOGGING_FILENAME
from enumClass.IsIgnoreType import IsIgnoreVendor
from enumClass.ReimburseType import ReimburseType
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class RedisGetHeaderAmountByBGService(IDataSerializer):

    def __init__(self, key, s_score, e_score):
        self.key = key
        self.s_score = s_score  # 當月1號
        self.e_score = e_score  # today
        self.db_no = 0
        self.reimburse_type = ReimburseType.ALL.value  # all:0

        logger.debug("------RedisGetHeaderAmountByBGService Param: ")
        logger.debug("key: " + str(self.key))  # key List
        logger.debug("score: " + str(self.s_score) + " ~ " + str(self.e_score))
        logger.debug("dbNo: " + str(self.db_no))
        logger.debug("isIgnoreVendor all: " + IsIgnoreVendor.YES.value + "," + IsIgnoreVendor.NO.value)    # Vendor 全部 (Y+N)
        logger.debug("Reimburse all: " + str(self.reimburse_type))

        connector = RedisConnector(REDIS_CONNECT_IP, None, REDIS_CONNECT_PWD, 6379, self.db_no)
        connector = connector.getConnectionInfo()
        self._connector = connector

    def serialize(self):
        apiJsonArr = {}
        try:
            sum_count = 0
            sumDataDict = {}  # key: yyyyMM+site, value: sum amount
            bgSet = set()
            rowKeyList = []
            rowKeyList.append(str(self.reimburse_type) + IsIgnoreVendor.YES.value)
            rowKeyList.append(str(self.reimburse_type) + IsIgnoreVendor.NO.value)

            for theKey in self.key:
                result = self._connector.zrangebyscore(theKey, self.s_score, self.e_score, withscores=True)
                logger.debug("====================")
                logger.debug("Key: " + theKey + ", zrangebyscore result: " + str(result))
                keySplit = theKey.split("_", 2)
                bg = keySplit[0]
                count = self._connector.zcount(theKey, self.s_score, self.e_score)
                logger.debug("Key: " + theKey + ", row data count: " + str(count))
                if count == 0:
                    continue
                sum_count += count

                # 解析Redis Json Value
                logger.debug("rowKey: " + str(rowKeyList))
                for data_json_tuple in result:  # result type is list
                    # data_json_tuple type is tuple
                    date_timestamp = datetime.fromtimestamp(data_json_tuple[1])
                    dateStr = date_timestamp.strftime('%Y%m%d')  # 日期yyyyMMdd
                    logger.debug("org timestamp: " + str(data_json_tuple[1]) + ", date_timestamp: " + str(date_timestamp))

                    data = data_json_tuple[0]
                    rowDataDict = json.loads(data)
                    logger.debug("rowDataDic: " + str(rowDataDict))

                    for rowKey in rowKeyList:
                        if rowKey in rowDataDict.keys():
                            dataDict = rowDataDict[rowKey]
                            dataKey = bg
                            # logger.debug("dataKey: " + dataKey)
                            if dataKey in sumDataDict.keys():
                                sumDataDict[dataKey] += dataDict['amount']
                            else:
                                sumDataDict[dataKey] = dataDict['amount']

                    bgSet.add(bg)  # 取得所有的site

            logger.debug("===BGSet : " + str(bgSet))
            logger.debug("===sum data count: " + str(sum_count))

            # 回傳API Json
            logger.debug("sumDataDic: " + str(sumDataDict))
            if bool(sumDataDict):  # 若Dict有資料

                # 根據site 和 date new 所有的殼
                mainObject = {}
                for bgSet_key in bgSet:
                    mainObject[bgSet_key] = sumDataDict[bgSet_key]

                apiJsonArr = json.dumps(mainObject, ensure_ascii=False)
                logger.info("dict轉JSON: " + str(apiJsonArr))
            else:
                apiJsonArr = None

        except Exception as ex:
            logger.error("Fail! Reason: " + traceback.format_exc())
            apiJsonArr = None

        finally:
            return apiJsonArr

