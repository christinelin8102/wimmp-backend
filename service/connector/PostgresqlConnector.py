#!/usr/bin/env python
import psycopg2

from service.connector.IConnection import IConnection


class PostgresqlConnector(IConnection):

    def getConnectionInfo(self):
        conn = psycopg2.connect(database=self._db, user=self._user, password=self._pwd, host=self._host, port=self._port)
        print("Opened database successfully")
        return conn
