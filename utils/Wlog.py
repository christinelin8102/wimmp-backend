import logging


class Wlog():

    def __init__(self,name):
        self.name = name
        '''
        初始化邮件发送对象
        :param receiver: 收件人：list 类型-['xxx@163.com','xxxx@qq.com']
        :param subject: 邮件标题
        '''

    @staticmethod
    def debug(data):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)

        return logger.debug(data)

    @staticmethod
    def info(self, data):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        logger.addHandler(ch)

        return logger.info(data)

    # def __init__(self, name):
    #     self.name = name
    #     logger = logging.getLogger(self.name)
    #     ch = logging.StreamHandler()
    #     formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
    #     # add formatter to ch
    #     ch.setFormatter(formatter)
    #     self.ch = ch
    #     logger.addHandler(self.ch)
    #     self.logger = logger
    #
    #
    # def debug(self, data):
    #     self.logger.setLevel(logging.DEBUG)  # cmd console
    #     self.ch.setLevel(logging.DEBUG)  # for python console
    #     self.logger.debug(data)
    #
    #
    # def info(self, data):
    #     self.logger.setLevel(logging.INFO)
    #     self.ch.setLevel(logging.INFO)
    #     self.logger.debug(data)
    #
    # def error(self, data):
    #     self.logger.setLevel(logging.ERROR)
    #     self.ch.setLevel(logging.ERROR)
    #     self.logger.error(data)
