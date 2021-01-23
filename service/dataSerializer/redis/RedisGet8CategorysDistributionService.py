import json
import traceback

from cfg.debug import REDIS_CONNECT_IP, REDIS_CONNECT_PWD, LOGGING_FILENAME
from service.connector.RedisConnector import RedisConnector
from service.dataSerializer.IDataSerializer import IDataSerializer
import logging

logger = logging.getLogger(__name__)

# User Home Page 4-2. 8-categorys Distribution Chart
class RedisGet8CategorysDistributionService(IDataSerializer):

    def __init__(self, key, start_score, end_score, vendor_type, reimburse_type):
        self.key = key
        self.s_score = start_score
        self.e_score = end_score
        self.db_no = 1
        self.vendor_type = vendor_type
        self.reimburse_type = reimburse_type

        logger.debug("------RedisGet8CategorysDistributionService Param: ")
        logger.debug("key: " + str(self.key))
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
            sumDataDict = {}  # key: category, value: sum amount
            sum_all_category_amount = 0  # 查詢總金額
            for theKey in self.key:
                result = self._connector.zrangebyscore(theKey, self.s_score, self.e_score, withscores=True)
                logger.debug("Key: " + theKey + ", zrangebyscore result: " + str(result))
                count = self._connector.zcount(theKey, self.s_score, self.e_score)
                logger.debug("Key: " + theKey + ", row data count: " + str(count))
                key_sum_amount = 0

                # 解析Redis Json Value
                rowKey = str(self.reimburse_type) + self.vendor_type
                logger.debug("rowKey: " + rowKey)
                for data_json_tuple in result:  # result type is list
                    # data_json_tuple type is tuple
                    data = data_json_tuple[0]

                    rowDataDict = json.loads(data)
                    logger.debug("rowDataDic: " + str(rowDataDict))
                    if rowKey in rowDataDict.keys():
                        dataDict = rowDataDict[rowKey]
                        for data in dataDict:
                            category = data.get('category', None)
                            if category is None:
                                continue
                            amount = data.get('amount', None)
                            if amount is None:
                                continue
                            sum_all_category_amount += amount
                            key_sum_amount += amount
                            if category in sumDataDict.keys():
                                sumDataDict[category] += amount
                            else:
                                sumDataDict[category] = amount
                    logger.debug("key_sum_amount: " + str(key_sum_amount))

                # 回傳API Json
                logger.debug("sum_all_category_amount: " + str(sum_all_category_amount))
                logger.debug("sumDataDic: " + str(sumDataDict))
                if bool(sumDataDict):  # 若Dict有資料
                    mainObject = {}
                    for key, value in sumDataDict.items():
                        subObject = {}
                        subObject["amount"] = value
                        subObject["percent"] = value / sum_all_category_amount
                        mainObject[key] = subObject
                    logger.info("dict轉JSON: " + str(mainObject))
                    apiJsonArr = json.dumps(mainObject, ensure_ascii=False)
                else:
                    apiJsonArr = None
        except Exception as ex:
            logger.error("Fail! Reason: " + traceback.format_exc())
            apiJsonArr = None

        finally:
            return apiJsonArr
