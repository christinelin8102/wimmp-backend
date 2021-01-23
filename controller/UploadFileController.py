import pandas as pd
from flask_restplus import Namespace, Resource, fields

from service.DashboardService import *
from service.UploadFileService import *
from io import StringIO
import csv

api = Namespace('uploadfile', description='upload Data')

uploadFileService = UploadFileService()

# period = api.model('period', {
#     'startdate': fields.Integer(required=True, description="startdate TimeStamp", help="startdate cannot be blank."),
#     'enddate': fields.Integer(required=True, description="enddate TimeStamp", help="enddate cannot be blank.")
# })
# request_fields = api.model('request_model', {
#     'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
#     'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
#     'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
#     'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
#     'site': fields.String(required=True, description="site", help="site cannot be blank."),
#     'plan': fields.String(required=True, description="plan", help="plan cannot be blank."),
#     'period': fields.Nested(period, description="period", help="period cannot be blank.")
# })



@api.route('', methods=["GET", "POST", "DELETE", "PUT"])
class UploadFileController(Resource):
    @api.route("/uploadPayment")
    class UploadPayment(Resource):
        def post(self):
            data = request.files['file'].read()
            # data = data.decode("utf-8")
            if data is None or data == '':
                return ApiResponse.emitErrorOutput(E_CREATE_FAIL, "無資料上傳", "no data")

            # result = []
            # column = ('Code', 'Payment_Term', 'Description')
            # for row in out:
            #     print(row)
            #     result.append(dict(zip(column, row)))

            return uploadFileService.uploadPaymentTerm(data)

    @api.route("/uploadVendor")
    class UploadVendor(Resource):
        def post(self):
            # print(request.data)
            # return "OK"
            # print(request.data)
            data = request.files['file'].read()
            if data is None or data == '':
                return ApiResponse.emitErrorOutput(E_CREATE_FAIL, "無資料上傳", "no data")

            # result = []
            # column = ('Code', 'Payment_Term', 'Description')
            # for row in out:
            #     print(row)
            #     result.append(dict(zip(column, row)))

            return uploadFileService.uploadVendorList(data)

    @api.route("/uploadExRate")
    class UploadPayment(Resource):
        def post(self):
            data = request.files['file'].read()
            data = data.decode("utf-8")
            if data is None or data == '':
                return ApiResponse.emitErrorOutput(E_CREATE_FAIL, "無資料上傳", "no data")

            return uploadFileService.upExRate(data)

    @api.route("/downloadPayment")
    class DownloadPayment(Resource):
        def get(self):
            return uploadFileService.downloadPaymentToCSV()

    @api.route("/downloadVendor")
    class DownloadVendor(Resource):
        def get(self):
            return uploadFileService.downloadVendorToCSV()
