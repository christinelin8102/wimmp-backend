ERROR_TEXT = "errorText"
ERROR_CODE = "errorCode"
ERROR_SOURCE = "errorSource"
REQUEST_STATUS = "status"
REQUEST_DATA = "data"
REQUEST_HEADER = "header"
SUCCESS_MSG = ""
OPERATION_SUCCESS = "Operation Failure QAQ~"
# 不存在指定的对象
E_CODE_OBJECT_NOT_EXISTS = 11
# 文件没有上传成功。
# E_CODE_UPLOAD_FAILED = 21
#
# E_CODE_USER_EXISTED = 104
# 员工已删除
E_CODE_USER_DELETED_ALREADY = 105
# 该职位不能登录
E_CODE_USER__TYPE_BAN = 106
E_CODE_PARAMETERS_BLANK = 201
# 数据效验失败
E_VALIDATION_ERROR = 12
# sql操作失败
E_SQLALCHEMY_ERROR = 13

# 新建用2开头
# 新建成功
E_CREATE_SUCCESS = 21
# 新建失败
E_CREATE_FAIL = 22
# 恢复（isdeleted字段）
E_RECOVERY_SUCCESS = 23
# 新增失败，已存在
E_CREATE_FAIL_EXISTS = 24

# 删除状态码已3开头
# 删除成功
E_DELETE_SUCCESS = 31
# 删除失败
E_DELETE_FAIL = 32
# 删除部分
E_DELETE_PARTIAL_FAIL = 33

# 查询状态码已4开头
# 查询成功
E_QUERY_SUCCESS = 41
# 查询失败
E_QUERY_FAIL = 42

# 修改状态码已5开头
# 修改成功
E_UPDATE_SUCCESS = 51
# 修改失败
E_UPDATE_FAIL = 52

# --------------------
# 操作成功 operation
E_OPERATION_SUCCESS = 0
# E_LOGIN_SUCCESS = 0
# 登陆失败
E_LOGIN_FAIL = 1
# 用户名或密码为空
E_CODE_USER_OR_PASSWORD_BLANK = 103
# 用户名或密码错误
E_CODE_USER_OR_PASSWORD_INVALID = 102
# 邮件发送成功
E_SEND_EMAIL_SUCCESS = 100
# 邮件发送失败
E_SEND_EMAIL_FAIL = 101
# 邮箱为空
E_EMAIL_BLANK = 104
# 未查询到相关用户
E_USER_BLANK = 105

# 密码修改成功
E_UPDATE_PASSWORD_SUCCESS = 106
# 密码修改失败
E_UPDATE_PASSWORD_FAIL = 107
# 链接已失效failure
E_URL_FAILURE = 108

# 数据存在exist
E_DATA_EXIST = 109

E_OPERATION_FAIL = 111

# 非法操作
E_ILLEGAL_OPERATION = 110
# 数据已被引用 无法删除
E_DATA_REFERENCED = 201

E_CODE_UPLOAD_FAILED = 21

# 邮件重复
E_EMAIL_EXIST = 120

# 用戶已刪除
E_USER_DELETEED = 121

R_STATUS_OK = "OK"
R_STATUS_FAIL = "FAIL"


class ApiResponse():

    @staticmethod
    def sendSuccess(email, enCode):
        return {
            "code": E_OPERATION_SUCCESS,
            "desc": "success",
            "errorSource": "",
            "data": {
                "email": email,
                "resetsToken": enCode
            }
        }

    @staticmethod
    def success(data):
        return {
            'code': E_OPERATION_SUCCESS,
            'desc': 'success',
            'data': data
        }

    @staticmethod
    def error(code, desc):
        return {
            "code": code,
            'desc': desc
        }

    @staticmethod
    def Illegal(code=E_ILLEGAL_OPERATION, desc="fail"):
        return {
            'code': code,
            'desc': desc
        }

    # 
    @staticmethod

    def emitErrorOutput(code,msg,source,httpcode=None,data={}):
        data = {
            ERROR_TEXT: msg,
            ERROR_CODE: code,
            ERROR_SOURCE: source,
            REQUEST_DATA: data,
            REQUEST_STATUS: R_STATUS_FAIL
        }
        if httpcode is None:
            return data
        else:
            return data, httpcode

    @staticmethod
    def emitSuccessOutput(data, dataheader=None, httpcode=None, code=E_OPERATION_SUCCESS, msg='', pageSize=None,
                          pageNo=None, totalPage=None, totalCount=None):
        if dataheader is None:
            data = {
                "result": {
                    "data": data,
                    "pageSize": pageSize,
                    "pageNo": pageNo,
                    "totalPage": totalPage,
                    "totalCount": totalCount
                }
            }
            if httpcode is None:
                return data
            else:
                return data, httpcode
        else:
            data = {
                "result": {
                    "data": data,
                    "pageSize": pageSize,
                    "pageNo": pageNo,
                    "totalPage": totalPage,
                    "totalCount": totalCount
                }
            }
            if httpcode is None:
                return data
            else:
                return data, httpcode

    @staticmethod
    def emitSuccessOutputAndLimit(data, httpcode=None, code=E_OPERATION_SUCCESS):
        data = {
            "code": code,
            REQUEST_DATA: data,
            REQUEST_STATUS: R_STATUS_OK,
            # "pages":pages
        }
        if httpcode is None:
            return data
        else:
            return data, httpcode
