from cfg.anko import *
import urllib

# ----------------------------Local SQLServer ------------------------------------#

DIALCT = "mssql"
DRIVER = "pymssql"
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

# ----------------------------AZure SQLServer ------------------------------------#
AZurelink = 'Server={},{};Database={};Uid={};Pwd={};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'. \
    format(AZUREHost, AZUREPort, AZUREDatabase, AZUREUser, AZurePass)
params = urllib.parse.quote_plus(r'Driver={ODBC Driver 17 for SQL Server};' + AZurelink)

# print(AZurelink)
AZUREDB_URI = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
if not AZURE_DATA_USAGE:
    AZUREDB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT, DRIVER, AZUREUser, AZurePass, AZUREHost,
                                                               AZUREPort, AZUREDatabase)

# ----------------Sqlalchemy connecting information  -----#
SQLALCHEMY_DATABASE_URI = DB_URI
if AZURE_DATA_USAGE:
    SQLALCHEMY_DATABASE_URI = AZUREDB_URI
JSON_AS_ASCII = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# file uploading storage path
MJD_FILEUPLOAD_SAVEPATH = 'static/upload/'
# file visiting path
MJD_FILEUPLOAD_VISITPATH = '/static/upload/'

REDIS_CONNECT_IP = '127.0.0.1'
REDIS_CONNECT_PWD = 'test'

POSTGRESQL_CONNECT_HOST = '127.0.0.1'
POSTGRESQL_CONNECT_ACCOUNT = 'test'
POSTGRESQL_CONNECT_PWD = 'test123'
POSTGRESQL_CONNECT_DB = 'mmp_dev'
POSTGRESQL_CONNECT_PROT = '5432'

POSTGRESQL_WISTRONCONNECT_HOST = '127.0.0.1'
POSTGRESQL_WISTRONCONNECT_ACCOUNT = 'test'
POSTGRESQL_WISTRONCONNECT_PWD = 'test123'
POSTGRESQL_WISTRONCONNECT_DB = 'test'
POSTGRESQL_WISTRONCONNECT_PROT = '5432'

LOGGING_FILENAME = 'logging_config.ini'
