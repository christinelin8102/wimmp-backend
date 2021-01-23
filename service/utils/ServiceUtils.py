import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

class ServiceUtils:

    @staticmethod
    def isMoreThanOneYear(startdate, enddate):
        endD = datetime.now()
        startD = endD - relativedelta(years=1)
        result = bool(
            startdate < startD.timestamp() or enddate < startD.timestamp() or
            startdate > endD.timestamp() or enddate > endD.timestamp())
        return result

