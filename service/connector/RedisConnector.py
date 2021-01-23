#!/usr/bin/env python
import redis

from service.connector.IConnection import IConnection


class RedisConnector(IConnection):

    def getConnectionInfo(self):
        pool = redis.ConnectionPool(host=self._host, port=self._port, db=self._db, password=self._pwd, decode_responses=True)
        r = redis.StrictRedis(connection_pool=pool)
        return r
