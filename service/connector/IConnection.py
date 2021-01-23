#!/usr/bin/env python
from __future__ import annotations

from abc import ABC, abstractmethod


class IConnection(ABC):

    def __init__(self, host, user, pwd, port, db):
        self._host = host
        self._user = user
        self._pwd = pwd
        self._port = port
        self._db = db

    @abstractmethod
    def getConnectionInfo(self):
        pass
