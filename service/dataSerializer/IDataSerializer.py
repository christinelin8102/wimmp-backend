#!/usr/bin/env python
from __future__ import annotations

from abc import ABC, abstractmethod


class IDataSerializer(ABC):

    def __init__(self, connector):
        self._connector = connector

    @abstractmethod
    def serialize(self):
        pass
