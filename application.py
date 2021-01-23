import os
import logging
from logging.config import fileConfig

from flask import Flask, request
from flask_cors import *
from flask_restplus import Api

from cfg.debug import LOGGING_FILENAME
from common.crmfilter import getSessionInfo, ApiResponse, E_CODE_USER_OR_PASSWORD_INVALID
from model.database import db
from utils import Cfg

from model.BG import ObjBG
from model.Charge import ObjCharge
from model.PaymentApplication import ObjPaymentApplication
from model.Plant import ObjPlant
from model.PurchaseOrder import ObjPurchaseOrder
from model.PurchaseOrderCharge import ObjPurchaseOrderCharge
from model.PurchaseOrderDetail import ObjPurchaseOrderDetail
from model.PurchaseRequest import ObjPurchaseRequest
from model.PurchaseRequestDetail import ObjPurchaseRequestDetail
from model.RT import ObjRT
from model.RTDetail import ObjRTDetail
from model.Site import ObjSite
from model.Vendor import ObjVendor
from model.PaymentTerm import ObjPaymentTerm
from model.ExchangeRate import ObjExchangeRate
from model.ExceptionAlert import ObjExceptionAlert

G_api = None

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.errorhandler(500)
def err_handler(e):
    return ApiResponse.emitErrorOutput(e.code, e.name, str(e.description))


@app.errorhandler(404)
def error_404(error):
    return ApiResponse.emitErrorOutput(error.code, error.name, '404 Not Found')

def exposeAPIs(pApi):
    from controller.DashboardController import api as dashboard
    from controller.UploadFileController import api as uploadfile
    from controller.ExceptionController import api as exception
    from controller.DashboardDailyMgtController import api as dailyMgtDashboard
    pApi.add_namespace(dashboard)
    pApi.add_namespace(uploadfile)
    pApi.add_namespace(exception)
    pApi.add_namespace(dailyMgtDashboard)


def initCfg(app):
    Cfg.MJD_FILEUPLOAD_SAVEPATH = app.config['MJD_FILEUPLOAD_SAVEPATH']
    Cfg.MJD_FILEUPLOAD_VISITPATH = app.config['MJD_FILEUPLOAD_VISITPATH']
    fileConfig(LOGGING_FILENAME, disable_existing_loggers=False)

def initRouting(app):
    authorizations = {
        'Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        },
    }
    G_api = Api(app, version='1.0', title=u'MMP',
                description=u'MMP', security='Bearer Auth', authorizations=authorizations
                )
    exposeAPIs(G_api)
    initCfg(app)


def initInterceptor(app):
    exclude_uris = {'/login', '/register', '/', '/swagger.json', '/user/login', '/functions/page'}

    @app.before_request
    def print_request_info():
        print(request.path.startswith('/swaggerui') == False)
        if (request.path not in exclude_uris) and getSessionInfo() == "" and request.path.startswith(
                '/swaggerui') == False and request.path.startswith('/static') == False:
            return ApiResponse.emitErrorOutput(E_CODE_USER_OR_PASSWORD_INVALID, u'Invalid user name or password',
                                               'login')


app.config.from_object('cfg.debug')
app.config['SECRET_KEY'] = 'itriedbutnoteasy'

POSTGRES = {
    'user': os.getenv('DB_USERNAME', 'admin_mmp@mmp-postgresql'),
    'pw': os.getenv('DB_PWD', 'Changeit!123'),
    'db': os.getenv('DB_NAME', 'mmp_dev'),
    'host': os.getenv('DB_HOST', 'mmp-postgresql.postgres.database.azure.com'),
    'port': os.getenv('DB_PORT', '5432'),
}

print('POSTGRES: ', POSTGRES)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

initRouting(app)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
