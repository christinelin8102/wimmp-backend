import json
from cfg.debug_mmp import POSTGRESQL_WISTRONCONNECT_HOST, POSTGRESQL_WISTRONCONNECT_ACCOUNT,\
    POSTGRESQL_WISTRONCONNECT_PWD,POSTGRESQL_WISTRONCONNECT_PROT, POSTGRESQL_WISTRONCONNECT_DB

from cfg.debug_mmp import POSTGRESQL_CONNECT_HOST, POSTGRESQL_CONNECT_ACCOUNT,\
    POSTGRESQL_CONNECT_PWD,POSTGRESQL_CONNECT_PROT, POSTGRESQL_CONNECT_DB

from service.connector.PostgresqlConnector import PostgresqlConnector
from service.dataSerializer.IDataSerializer import IDataSerializer


# from model.PurchaseOrder import ObjPurchaseOrder
# from model.PurchaseOrderLine import ObjPurchaseOrderLine


class GetDataService(IDataSerializer):

    def __init__(self):
        pass

    def getdata(self, sqlquery):
        connector = PostgresqlConnector(POSTGRESQL_CONNECT_HOST, POSTGRESQL_CONNECT_ACCOUNT,
                                        POSTGRESQL_CONNECT_PWD, POSTGRESQL_CONNECT_PROT, POSTGRESQL_CONNECT_DB)
        connector = connector.getConnectionInfo()
        cursor = connector.cursor()
        cursor.execute(sqlquery)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getwistrondata(self, sqlquery):
        connector = PostgresqlConnector(POSTGRESQL_WISTRONCONNECT_HOST, POSTGRESQL_WISTRONCONNECT_ACCOUNT,
                                        POSTGRESQL_WISTRONCONNECT_PWD,
                                        POSTGRESQL_WISTRONCONNECT_PROT, POSTGRESQL_WISTRONCONNECT_DB)
        connector = connector.getConnectionInfo()
        cursor = connector.cursor()
        cursor.execute(sqlquery)
        result = cursor.fetchall()
        cursor.close()
        return result
