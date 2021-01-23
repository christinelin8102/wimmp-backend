import os

from dateutil.relativedelta import relativedelta
from flask import url_for
from flask_restplus import Namespace, Resource, fields
from werkzeug.utils import secure_filename

from service.DashboardService import *
from service.ExceptionService import *
from utils.Cfg import MJD_FILEUPLOAD_SAVEPATH
from utils.ControllerUtils import *

api = Namespace('exception', description='exception Data')

exceptionService = ExceptionService()

period = api.model('period', {
    'startdate': fields.Integer(required=True, description="startdate TimeStamp", help="startdate cannot be blank."),
    'enddate': fields.Integer(required=True, description="enddate TimeStamp", help="enddate cannot be blank.")
})
request_fields = api.model('request_model', {
    'vendor': fields.Boolean(required=True, description="vendor", help="vendor cannot be blank."),
    'reimburse': fields.Boolean(required=True, description="reimburse", help="reimburse cannot be blank."),
    'nonreimburse': fields.Boolean(required=True, description="nonreimburse", help="nonreimburse cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank.")
})
request_page_fields = api.model('request_page_model', {
    'paymentterm': fields.String(required=True, description="paymentterm", help="paymentterm cannot be blank."),
    'process': fields.Boolean(required=True, description="process", help="process cannot be blank."),
    'notprocess': fields.Boolean(required=True, description="notprocess", help="notprocess cannot be blank."),
    'bg': fields.String(required=True, description="bg", help="bg cannot be blank."),
    'site': fields.String(required=True, description="site", help="site cannot be blank."),
    'plant': fields.String(required=True, description="plant", help="plant cannot be blank."),
    'period': fields.Nested(period, description="period", help="period cannot be blank."),
    'pageSize': fields.Integer(required=True, description="pageSize", help="pageSize cannot be blank."),
    'pageNo': fields.Integer(required=True, description="pageNo TimeStamp", help="pageNo cannot be blank.")
})

ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])


@api.route('', methods=["GET", "POST", "DELETE", "PUT"])
class ExceptionController(Resource):
    @api.route("/alertReports")
    class getExceptionAlertReport(Resource):
        @api.expect(request_page_fields)
        def post(self):
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBodyExcept(data)
            return exceptionService.getExceptionAlertReportList(req)

    @api.route("/alerts")
    class getExceptionAlert(Resource):
        @api.expect(request_page_fields)
        def post(self):
            data = request.get_json()
            if data is None:
                return "請求參數不能為空"
            req = ControllerUtils.handleRequestBodyExcept(data)
            return exceptionService.getExceptionAlertList(req)

    @api.route("/alert/<id>")
    class getExceptionAlertByAlertID(Resource):
        def get(self, id):
            return exceptionService.getExceptionAlertByID(id)

    @api.route("/process")
    class processExceptionAlert(Resource):
        @api.expect(
            api.model('process_alert_model', {
                'alert_id': fields.String(required=True, description="alert_id", help=""),
                'is_reasonable': fields.Boolean(required=False, description="file_url", help=""),
                'file_url': fields.String(required=False, description="file_url", help=""),
                'note': fields.String(required=False, description="note", help="")
            }))
        def post(self):
            data = request.get_json()
            alert_id = data.get('alert_id', None)
            is_reasonable = data.get('is_reasonable', False)
            file_url = data.get('file_url', None)
            note = data.get('note', None)
            if alert_id is None:
                return ApiResponse.emitErrorOutput(E_CREATE_FAIL, "缺少參數", "Process Exception Alert")
            return exceptionService.processExceptionAlert(alert_id, is_reasonable, file_url, note)

    @api.route("/uploadFile/<id>")
    class uploadExceptionFile(Resource):
        def post(self, id):

            id = id
            files = request.files.getlist('file')
            file_list = []
            for file in files:
                if file and self.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                else:
                    return ApiResponse.emitErrorOutput(E_CODE_UPLOAD_FAILED, "上傳失敗或檔案名稱錯誤", "Upload File")
                if not os.path.isdir(MJD_FILEUPLOAD_SAVEPATH):
                    os.mkdir(MJD_FILEUPLOAD_SAVEPATH)
                savepath = os.path.join(MJD_FILEUPLOAD_SAVEPATH, filename)
                file.save(savepath)
                file_list.append(filename)
            return exceptionService.saveExceptionAlertFile(id, file_list)


        def allowed_file(self, filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @api.route("/downloadFile/<id>")
    class downloadExceptionFile(Resource):
        def get(self, id):
            return exceptionService.downloadExceptionFileByID(id)
