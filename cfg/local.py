# DIALCT = "mssql"
# DRIVER = "pymssql"
# USERNAME = "sa"
# PASSWORD = "pigu123"
# HOST = "127.0.0.1"
# PORT = "1433"
# DATABASE = "mjd_crm"
# DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# JSON_AS_ASCII = False
# SQLALCHEMY_TRACK_MODIFICATIONS = False
#
# MJD_DIALCT = "mssql"
# MJD_DRIVER = "pymssql"
# MJD_HOST = "39.108.191.100"
# MJD_PORT = "1433"
# MJD_USERNAME = "sa"
# MJD_PASSWORD = "wr2018!@#"
# MJD_DATABASE_BIZ = "medjaden_biz"
# MJD_DATABASE_SYS = "medjaden_sys"
# MJD_BIZ_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(MJD_DIALCT,MJD_DRIVER,MJD_USERNAME,MJD_PASSWORD,MJD_HOST,MJD_PORT,MJD_DATABASE_BIZ)
# MJD_SYS_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(MJD_DIALCT,MJD_DRIVER,MJD_USERNAME,MJD_PASSWORD,MJD_HOST,MJD_PORT,MJD_DATABASE_SYS)
#
# SQLALCHEMY_BINDS = {
#     'mjd_biz': MJD_BIZ_URI,
#     'mjd_sys': MJD_SYS_URI
# }

#文件保存路径
MJD_FILEUPLOAD_SAVEPATH = 'static/upload/'
#文件访问路径
MJD_FILEUPLOAD_VISITPATH = '/static/upload/'