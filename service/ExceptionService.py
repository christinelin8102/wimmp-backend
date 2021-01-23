import json
import traceback
import random
import logging
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from common.crmfilter import *
from model.ExceptionAlert import ObjExceptionAlert
from view.ExceptionAlert import ExceptionAlertSchema
from view.ExceptionAlertReport import ExceptionAlertReportSchema
from view.Exception import ExceptionSchema

logger = logging.getLogger(__name__)

objExceptionAlert = ObjExceptionAlert()
exceptionAlertSchema = ExceptionAlertSchema()
exceptionAlertReportSchema = ExceptionAlertReportSchema()
exceptionSchema = ExceptionSchema()


class ExceptionService:

    def getExceptionAlertList(self, req):
        paymentterm = req.paymentterm
        processTag = req.processTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        search_key = req.search_key
        page = req.pageNo
        size = req.pageSize
        ft = [ObjExceptionAlert.plant_code.in_(plan)]
        pagination = ObjExceptionAlert.query.filter(*ft). \
            order_by(ObjExceptionAlert.alert_id). \
            paginate(1, per_page=10, error_out=False)

        result = exceptionAlertSchema.dump(pagination.items, many=True)

        return ApiResponse.emitSuccessOutput(data=result, pageSize=size, pageNo=page, totalCount=pagination.total,
                                             totalPage=pagination.pages)

    def getExceptionAlertByID(self, alert_id):  # plan B exceptionAlertList call exceptionAlertByAlertID
        exceptionAlert = ObjExceptionAlert.query.filter(ObjExceptionAlert.alert_id == alert_id).first()
        if exceptionAlert is None or exceptionAlert == '':
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "無法找到指定id的Exception", "Exception List")
        else:
            result = exceptionSchema.dump(exceptionAlert)
        return ApiResponse.emitSuccessOutput(result)

    def processExceptionAlert(self, alert_id, is_reasonable, file_url, note):

        ExceptionAlert = ObjExceptionAlert.query.filter(ObjExceptionAlert.alert_id == alert_id).first()
        if ExceptionAlert is None or ExceptionAlert == '':
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "無法找到指定id的Exception", "Exception List")
        else:
            ExceptionAlert.files_link = file_url
            ExceptionAlert.is_reasonable = is_reasonable
            ExceptionAlert.notes = note
            ExceptionAlert.update()
        return ApiResponse.emitSuccessOutput("commit exception_alert success")

    def getExceptionAlertReportList(self, req):
        paymentterm = req.paymentterm
        processTag = req.processTag
        bg = req.bg
        site = req.site
        plan = req.plant
        startdate = req.startdate
        enddate = req.enddate
        page = req.pageNo
        size = req.pageSize
        ft = []
        ft = [ObjExceptionAlert.plant_code.in_(plan), ObjExceptionAlert.processed_by != '']
        pagination = ObjExceptionAlert.query.filter(*ft).order_by(ObjExceptionAlert.alert_id).paginate(page,
                                                                                                       per_page=size,
                                                                                                       error_out=False)

        result = exceptionAlertReportSchema.dump(pagination.items, many=True)
        return ApiResponse.emitSuccessOutput(data=result, pageSize=size, pageNo=page, totalCount=pagination.total,
                                             totalPage=pagination.pages)

    def saveExceptionAlertFile(self, id, file_list):
        files_link = ''
        count = 0
        ExceptionAlert = ObjExceptionAlert.query.filter(ObjExceptionAlert.alert_id == int(id)).first()
        if ExceptionAlert is None or ExceptionAlert == '':
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "無法找到指定id的Exception", "Exception List")
        else:
            for file in file_list:
                files_link = files_link + file + ';'
                count += 1
            files_link[:-1]
            ExceptionAlert.files_link = files_link
            ExceptionAlert.update()

        return ApiResponse.emitSuccessOutput("save " + str(count) + " files")

    def downloadExceptionFileByID(self, id):
        ExceptionAlert = ObjExceptionAlert.query.filter(ObjExceptionAlert.alert_id == id).first()
        if ExceptionAlert is None or ExceptionAlert == '':
            return ApiResponse.emitErrorOutput(E_QUERY_FAIL, "無法找到指定id的Exception", "Exception List")
        else:
            files = ExceptionAlert.files_link
            fileList = []
            if files.find(';'):
                fileList = files.split(';')
            else:
                fileList.append(files)
            #TODO download file and zip

        return 1
